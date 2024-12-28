'''
   Copyright 2024 Nils Kopal, Bernhard Esslinger, CrypTool Team

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

import gzip
import struct
import numpy as np

class LanguageStatisticsFile:
    """
    Class for handling the loading of language statistics from a compressed file.

    Attributes:
    - FILE_FORMAT_MAGIC_NUMBER (str): The expected magic number to identify valid language statistics files.
    - file_path (str): The path to the language statistics file.
    - alphabet (str): The alphabet used in the language statistics.
    - language_code (str): The language code extracted from the statistics file.
    """

    FILE_FORMAT_MAGIC_NUMBER = "CTLS"

    def __init__(self, file_path):
        """
        Initializes the LanguageStatisticsFile class.

        Parameters:
        - file_path (str): The path to the language statistics file.

        Initializes:
        - self.file_path (str): Stores the path to the file.
        - self.alphabet (str): Initially empty, set after file loading.
        - self.language_code (str): Initially empty, set after file loading.
        """
        self.file_path = file_path
        self.alphabet = ''
        self.language_code = ''

    def load_frequencies(self, array_dimensions):
        """
        Loads the frequency data from the language statistics file.

        Parameters:
        - array_dimensions (int): The dimensionality of the frequency array (e.g., 1 for unigrams, 2 for bigrams).

        Returns:
        - np.ndarray: A numpy array containing the frequency data.

        Raises:
        - Exception: If the file format is invalid or the dimensions of the frequency array do not match the expected value.

        Process:
        1. Validates the file by checking the magic number.
        2. Reads the language code, gram length, and alphabet.
        3. Verifies that the gram length matches the required dimensions.
        4. Reads the frequency data and reshapes it into the appropriate numpy array format.
        5. Copies the data into a new numpy array to allow modification.
        """
        with gzip.open(self.file_path, 'rb') as file:
            # Validate the file format by checking the magic number.
            magic_number = file.read(4).decode('utf-8')
            if magic_number != self.FILE_FORMAT_MAGIC_NUMBER:
                raise Exception("File does not start with the expected magic number for language statistics.")

            # Read the language code (length-prefixed string).
            language_code_length_bytes = file.read(1)[0]
            self.language_code = file.read(language_code_length_bytes).decode('utf-8')

            # Read the gram length (32-bit signed integer).
            gram_length = struct.unpack('<i', file.read(4))[0]

            # Ensure the gram length matches the required dimensions.
            if gram_length != array_dimensions:
                raise Exception("Gram length of statistics file differs from required dimensions of frequency array.")

            # Read the alphabet (length-prefixed string).
            self.alphabet_length = file.read(1)[0]
            self.alphabet = file.read(self.alphabet_length).decode('utf-8')

            # Calculate the total number of frequency entries.
            frequency_entries = self.alphabet_length ** gram_length

            # Read the frequency data (32-bit float array).
            frequency_data = file.read(frequency_entries * 4)

            # Reshape the data into the correct dimensionality and copy it for mutability.
            if array_dimensions == 1:
                frequencies = np.frombuffer(frequency_data, dtype=np.float32).copy()
            else:
                frequencies = np.frombuffer(frequency_data, dtype=np.float32).reshape(
                    tuple([self.alphabet_length] * array_dimensions)
                ).copy()

            return frequencies
