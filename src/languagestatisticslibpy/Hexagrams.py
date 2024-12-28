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
import numpy as np
import os
from languagestatisticslibpy.Grams import Grams
from languagestatisticslibpy.GramsType import GramsType
from languagestatisticslibpy.LanguageStatisticsFile import LanguageStatisticsFile

class Hexagrams(Grams):
    def __init__(self, language, language_statistics_directory, use_spaces=False):
        """
        Initializes the Hexagrams class by calling the parent class (Grams) initializer.

        Parameters:
        - language (str): The language of the hexagram statistics.
        - language_statistics_directory (str): Path to the directory containing language statistics files.
        - use_spaces (bool): Whether to include spaces in the analysis (default: False).
        """
        super().__init__(language, language_statistics_directory, use_spaces)

    def load_gz(self, filename, language_statistics_directory):
        """
        Loads a gzip-compressed file containing hexagram frequencies.

        Parameters:
        - filename (str): The name of the file to load.
        - language_statistics_directory (str): The directory where the statistics file is located.

        Sets:
        - self.frequencies (np.ndarray): A 6D array of hexagram frequencies.
        - self.alphabet (list): The alphabet used in the statistics file.
        - self.max_value (float): The maximum value in the frequencies array, or -∞ if the array is empty.
        """
        file_path = os.path.join(language_statistics_directory, filename)
        language_statistics_file = LanguageStatisticsFile(file_path)
        self.frequencies = language_statistics_file.load_frequencies(6)
        self.alphabet = language_statistics_file.alphabet
        self.max_value = np.max(self.frequencies) if self.frequencies.size > 0 else float('-inf')

    def calculate_cost(self, text):
        """
        Calculates the cost of a given text based on hexagram frequencies.

        Parameters:
        - text (str): The text to analyze.

        Returns:
        - float: The average cost of hexagrams in the text. Returns 0.0 if the text length is less than 6.

        Notes:
        - Skips hexagrams containing characters outside the defined alphabet.
        - If `add_letter_indices` is defined, modifies the index of the characters before computing the cost.
        """
        if len(text) < 6:
            return 0.0

        value = 0.0
        alphabet_length = len(self.alphabet)
        end = len(text) - 5

        for i in range(end):
            a, b, c, d, e, f = text[i:i+6]

            if self.add_letter_indices:
                a += self.add_letter_indices.get(a, 0)
                b += self.add_letter_indices.get(b, 0)
                c += self.add_letter_indices.get(c, 0)
                d += self.add_letter_indices.get(d, 0)
                e += self.add_letter_indices.get(e, 0)
                f += self.add_letter_indices.get(f, 0)

            if 0 <= a < alphabet_length and 0 <= b < alphabet_length and \
               0 <= c < alphabet_length and 0 <= d < alphabet_length and \
               0 <= e < alphabet_length and 0 <= f < alphabet_length:
                value += self.frequencies[a, b, c, d, e, f]

        return value / end

    def gram_size(self):
        """
        Returns the size of the grams being analyzed (hexagrams in this case).

        Returns:
        - int: The size of the grams (always 6 for hexagrams).
        """
        return 6

    def grams_type(self):
        """
        Returns the type of grams being analyzed.

        Returns:
        - GramsType: An enum value representing the type of grams (GramsType.Hexagrams).
        """
        return GramsType.Hexagrams

    def normalize(self, max_value):
        """
        Normalizes the hexagram frequencies based on the provided maximum value.

        Parameters:
        - max_value (float): The maximum value used for normalization.

        Notes:
        - Adjusts all frequencies proportionally to the new maximum value.
        - Updates `self.max_value` to the new maximum after normalization.
        """
        super().normalize(max_value)
        adjust_value = self.max_value * max_value
        for a in range(len(self.alphabet)):
            for b in range(len(self.alphabet)):
                for c in range(len(self.alphabet)):
                    for d in range(len(self.alphabet)):
                        for e in range(len(self.alphabet)):
                            for f in range(len(self.alphabet)):
                                self.frequencies[a, b, c, d, e, f] = adjust_value / self.frequencies[a, b, c, d, e, f]
        self.max_value = np.max(self.frequencies) if self.frequencies.size > 0 else float('-inf')
