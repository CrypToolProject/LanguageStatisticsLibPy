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
import numpy as np
import os
from languagestatisticslibpy.Grams import Grams
from languagestatisticslibpy.GramsType import GramsType
from languagestatisticslibpy.LanguageStatisticsFile import LanguageStatisticsFile

class Pentagrams(Grams):
    def __init__(self, language, language_statistics_directory, use_spaces=False):
        super().__init__(language, language_statistics_directory, use_spaces)

    def load_gz(self, filename, language_statistics_directory):
        file_path = os.path.join(language_statistics_directory, filename)
        language_statistics_file = LanguageStatisticsFile(file_path)
        self.frequencies = language_statistics_file.load_frequencies(5)
        self.alphabet = language_statistics_file.alphabet
        self.max_value = np.max(self.frequencies) if self.frequencies.size > 0 else float('-inf')

    def calculate_cost(self, text):
        if len(text) < 5:
            return 0.0

        value = 0.0
        alphabet_length = len(self.alphabet)
        end = len(text) - 4

        for i in range(end):
            a, b, c, d, e = text[i:i+5]

            if self.add_letter_indices:
                a += self.add_letter_indices.get(a, 0)
                b += self.add_letter_indices.get(b, 0)
                c += self.add_letter_indices.get(c, 0)
                d += self.add_letter_indices.get(d, 0)
                e += self.add_letter_indices.get(e, 0)

            if 0 <= a < alphabet_length and 0 <= b < alphabet_length and \
               0 <= c < alphabet_length and 0 <= d < alphabet_length and \
               0 <= e < alphabet_length:
                value += self.frequencies[a, b, c, d, e]

        return value / end

    def gram_size(self):
        return 5

    def grams_type(self):
        return GramsType.Pentagrams
    
    def normalize(self, max_value):
        super().normalize(max_value)
        adjust_value = self.max_value * max_value
        for a in range(len(self.alphabet)):
            for b in range(len(self.alphabet)):
                for c in range(len(self.alphabet)):
                    for d in range(len(self.alphabet)):
                        for e in range(len(self.alphabet)):
                            self.frequencies[a, b, c, d, e] = adjust_value / self.frequencies[a, b, c, d, e]
        self.max_value = np.max(self.frequencies) if self.frequencies.size > 0 else float('-inf')              
