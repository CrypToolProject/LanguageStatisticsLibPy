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

class Bigrams(Grams):
    def __init__(self, language, language_statistics_directory, use_spaces=False):
        super().__init__(language, language_statistics_directory, use_spaces)

    def load_gz(self, filename, language_statistics_directory):
        file_path = os.path.join(language_statistics_directory, filename)
        language_statistics_file = LanguageStatisticsFile(file_path)
        self.frequencies = language_statistics_file.load_frequencies(2)
        self.alphabet = language_statistics_file.alphabet
        self.max_value = np.max(self.frequencies) if self.frequencies.size > 0 else float('-inf')

    def calculate_cost(self, text):
        if len(text) < 2:
            return 0

        value = 0
        alphabet_length = len(self.alphabet)
        end = len(text) - 1

        for i in range(end):
            a = text[i]
            b = text[i + 1]

            if self.add_letter_indices:
                a += self.add_letter_indices[a]
                b += self.add_letter_indices[b]

            if a >= alphabet_length or b >= alphabet_length or a < 0 or b < 0:
                continue
            value += self.frequencies[a, b]

        return value / end

    def gram_size(self):
        return 2

    def grams_type(self):
        return GramsType.Bigrams

    def normalize(self, max_value):
        super().normalize(max_value)
        adjust_value = self.max_value * max_value
        for a in range(len(self.alphabet)):
            for b in range(len(self.alphabet)):
                self.frequencies[a, b] = adjust_value / self.frequencies[a, b]
        self.max_value = np.max(self.frequencies) if self.frequencies.size > 0 else float('-inf')
