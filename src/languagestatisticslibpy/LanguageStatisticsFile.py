'''
   Copyright 2024 Nils Kopal, CrypTool Team

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
'''
import struct
import numpy as np
import gzip

class LanguageStatisticsFile:
    FILE_FORMAT_MAGIC_NUMBER = "CTLS"

    def __init__(self, file_path):
        self.file_path = file_path
        self.alphabet = ''
        self.language_code = ''

    def load_frequencies(self, array_dimensions):
        with gzip.open(self.file_path, 'rb') as file:
            magic_number = file.read(4).decode('utf-8')
            if magic_number != self.FILE_FORMAT_MAGIC_NUMBER:
                raise Exception("File does not start with the expected magic number for language statistics.")
            
            #read language code, which is a string with a length prefix of 1 byte
            language_code_length_bytes = file.read(1)[0]
            self.language_code = file.read(language_code_length_bytes).decode('utf-8')
            
            #read gram length which is a 32-bit signed integer
            gram_length = struct.unpack('<i', file.read(4))[0]
            
            if gram_length != array_dimensions:
                raise Exception("Gram length of statistics file differs from required dimensions of frequency array.")
            
            #read alphabet which is a string with a length prefix
            self.alphabet_length = file.read(1)[0]
            self.alphabet = file.read(self.alphabet_length).decode('utf-8')
            
            #now read frequency data which is a 32-bit float array
            frequency_entries = self.alphabet_length ** gram_length
            frequency_data = file.read(frequency_entries * 4)
            
            #we have to copy the data into a new numpy array. If we don't do this, we cannot normalize the data since it is read-only
            if array_dimensions == 1:
                frequencies = np.frombuffer(frequency_data, dtype=np.float32).copy()
            else:
                frequencies = np.frombuffer(frequency_data, dtype=np.float32).reshape(tuple([self.alphabet_length] * array_dimensions)).copy()
            
            return frequencies