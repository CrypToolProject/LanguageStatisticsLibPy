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
from abc import ABC, abstractmethod

class Grams(ABC):
    def __init__(self, language, language_statistics_directory, use_spaces):
        self.max_value = None
        self.is_normalized = False
        self.alphabet = None
        self.add_letter_indices = None

        filename = f"{language}-{self.gram_size()}gram-nocs{'-sp' if use_spaces else ''}.gz"        
        try:
            self.load_gz(filename, language_statistics_directory)
        except FileNotFoundError as e:
            raise Exception(f"Did not find the specified language statistics file for language={language} and use_spaces={use_spaces}: {filename}") from e

    @abstractmethod
    def calculate_cost(self, text):
        ...
    
    @abstractmethod
    def gram_size(self):
        ...

    @abstractmethod
    def grams_type(self):
        ...

    @abstractmethod
    def load_gz(self, filename, language_statistics_directory):
        ...

    def reduce_alphabet(self, new_alphabet):
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
        if self.is_normalized:
            raise Exception("This Gram object has already been normalized!")
        self.is_normalized = True