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
from abc import ABC, abstractmethod

class Grams(ABC):
    def __init__(self, language, language_statistics_directory, use_spaces):
        """
        Initializes the Grams superclass.

        Parameters:
        - language (str): The language of the n-gram statistics.
        - language_statistics_directory (str): Path to the directory containing language statistics files.
        - use_spaces (bool): Whether to include spaces in the analysis.

        Initializes:
        - self.max_value (float): The maximum value of the frequencies, set during file loading.
        - self.is_normalized (bool): Tracks whether the frequencies have been normalized.
        - self.alphabet (list): The alphabet used in the statistics file.
        - self.add_letter_indices (list): Adjustment indices for characters when reducing the alphabet.

        Raises:
        - Exception: If the specified language statistics file is not found.
        """
        self.max_value = None
        self.is_normalized = False
        self.alphabet = None
        self.add_letter_indices = None

        # Construct the filename based on language and space usage.
        filename = f"{language}-{self.gram_size()}gram-nocs{'-sp' if use_spaces else ''}.gz"
        try:
            # Attempt to load the gzipped language statistics file.
            self.load_gz(filename, language_statistics_directory)
        except FileNotFoundError as e:
            raise Exception(f"Did not find the specified language statistics file for language={language} and use_spaces={use_spaces}: {filename}") from e

    @abstractmethod
    def calculate_cost(self, text):
        """
        Abstract method to calculate the cost of a given text based on n-gram frequencies.

        Parameters:
        - text (str): The text to analyze.

        Returns:
        - float: The calculated cost of the text.
        """
        ...

    @abstractmethod
    def gram_size(self):
        """
        Abstract method to return the size of the grams (e.g., 1 for unigrams, 2 for bigrams).

        Returns:
        - int: The size of the grams.
        """
        ...

    @abstractmethod
    def grams_type(self):
        """
        Abstract method to return the type of grams (e.g., GramsType.Unigrams).

        Returns:
        - GramsType: An enum representing the type of grams.
        """
        ...

    @abstractmethod
    def load_gz(self, filename, language_statistics_directory):
        """
        Abstract method to load a gzipped file containing n-gram frequencies.

        Parameters:
        - filename (str): The name of the file to load.
        - language_statistics_directory (str): The directory where the statistics file is located.

        Raises:
        - FileNotFoundError: If the file does not exist.
        """
        ...

    def reduce_alphabet(self, new_alphabet):
        """
        Reduces the current alphabet to a new, smaller alphabet.

        Parameters:
        - new_alphabet (list): The reduced alphabet.

        Notes:
        - If the new alphabet matches the original alphabet in size, no changes are made.
        - Updates `self.add_letter_indices` to reflect adjustments for the reduced alphabet.
        """
        if len(new_alphabet) == len(self.alphabet):
            self.add_letter_indices = None
            return

        self.add_letter_indices = [0] * len(new_alphabet)
        add_value = 0
        for i, letter in enumerate(new_alphabet):
            if letter not in self.alphabet:
                add_value += 1
            self.add_letter_indices[i] = add_value

    def normalize(self, max_value):
        """
        Normalizes the n-gram frequencies to a specified maximum value.

        Parameters:
        - max_value (float): The maximum value for normalization.

        Raises:
        - Exception: If the frequencies have already been normalized.

        Notes:
        - Sets `self.is_normalized` to True after normalization.
        """
        if self.is_normalized:
            raise Exception("This Gram object has already been normalized!")
        self.is_normalized = True