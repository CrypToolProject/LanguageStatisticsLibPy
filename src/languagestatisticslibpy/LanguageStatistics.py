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
import os
import gzip
from enum import Enum
from languagestatisticslibpy.GramsType import GramsType
from languagestatisticslibpy.Unigrams import Unigrams
from languagestatisticslibpy.Bigrams import Bigrams
from languagestatisticslibpy.Trigrams import Trigrams
from languagestatisticslibpy.Tetragrams import Tetragrams
from languagestatisticslibpy.Pentagrams import Pentagrams
from languagestatisticslibpy.Hexagrams import Hexagrams
from languagestatisticslibpy.WordTree import WordTree

class HandlingOfUnknownSymbols(Enum):
    """
    Enum to specify how to handle unknown symbols during text or number mapping.

    Attributes:
    - REMOVE (int): Remove unknown symbols.
    - REPLACE (int): Replace unknown symbols with a specific character or number.
    """
    REMOVE = 0
    REPLACE = 1


class LanguageStatistics:
    """
    Provides utilities for handling language-related statistics, such as unigram frequencies,
    alphabet definitions, and mapping between text and number spaces.

    Attributes:
    - supported_languages_codes (list): A list of ISO language codes for supported languages.
    - supported_languages (list): A list of language names corresponding to the supported language codes.
    - unigrams (dict): A dictionary mapping language codes to their unigram frequencies.
    - alphabets (dict): A dictionary mapping language codes to their alphabets.
    """

    supported_languages_codes = [
        "en", "de", "es", "fr", "it", "hu", "ru", "cs", "el", "la", "nl", "sv", "pt", "pl", "tr"
    ]

    supported_languages = [
        "English", "German", "Spanish", "French", "Italian", "Hungarian",
        "Russian", "Czech", "Greek", "Latin", "Dutch", "Swedish",
        "Portuguese", "Polish", "Turkish"
    ]

    unigrams = {
        # Source: Wikipedia
        "en": [ 0.08167, 0.01492, 0.02782, 0.04253, 0.12702, 0.02228, 0.02015, 0.06094, 0.06966, 0.00153, 0.00772, 0.04025, 0.02406, 0.06749, 0.07507, 0.01929, 0.00095, 0.05987, 0.06327, 0.09056, 0.02758, 0.00978, 0.0236, 0.0015, 0.01974, 0.00074], # English
        "fr": [ 0.07636, 0.00901, 0.0326, 0.03669, 0.14715, 0.01066, 0.00866, 0.00737, 0.07529, 0.00613, 0.00049, 0.05456, 0.02968, 0.07095, 0.05796, 0.02521, 0.01362, 0.06693, 0.07948, 0.07244, 0.06311, 0.01838, 0.00074, 0.00427, 0.00128, 0.00326], # French
        "de": [ 0.06516, 0.01886, 0.02732, 0.05076, 0.16396, 0.01656, 0.03009, 0.04577, 0.0655, 0.00268, 0.01417, 0.03437, 0.02534, 0.09776, 0.02594, 0.0067, 0.00018, 0.07003, 0.0727, 0.06154, 0.04166, 0.00846, 0.01921, 0.00034, 0.00039, 0.01134], # German
        "es": [ 0.11525, 0.02215, 0.04019, 0.0501, 0.12181, 0.00692, 0.01768, 0.00703, 0.06247, 0.00493, 0.00011, 0.04967, 0.03157, 0.06712, 0.08683, 0.0251, 0.00877, 0.06871, 0.07977, 0.04632, 0.02927, 0.01138, 0.00017, 0.00215, 0.01008, 0.00467], # Spanish
        "pt": [ 0.14634, 0.01043, 0.03882, 0.04992, 0.1257, 0.01023, 0.01303, 0.00781, 0.06186, 0.00397, 0.00015, 0.02779, 0.04738, 0.04446, 0.09735, 0.02523, 0.01204, 0.0653, 0.06805, 0.04336, 0.03639, 0.01575, 0.00037, 0.00253, 6e-005, 0.0047], # Portuguese
        "eo": [ 0.12117, 0.0098, 0.00776, 0.03044, 0.08995, 0.01037, 0.01171, 0.00384, 0.10012, 0.03501, 0.04163, 0.06104, 0.02994, 0.07955, 0.08779, 0.02755, 0, 0.05914, 0.06092, 0.05276, 0.03183, 0.01904, 0, 0, 0, 0.00494], # Esperanto
        "it": [ 0.11745, 0.00927, 0.04501, 0.03736, 0.11792, 0.01153, 0.01644, 0.00636, 0.10143, 0.00011, 9e-005, 0.0651, 0.02512, 0.06883, 0.09832, 0.03056, 0.00505, 0.06367, 0.04981, 0.05623, 0.03011, 0.02097, 0.00033, 3e-005, 0.0002, 0.01181], # Italian
        "tr": [ 0.1292, 0.02844, 0.01463, 0.05206, 0.09912, 0.00461, 0.01253, 0.01212, 0.096, 0.00034, 0.05683, 0.05922, 0.03752, 0.07987, 0.02976, 0.00886, 0, 0.07722, 0.03014, 0.03314, 0.03235, 0.00959, 0, 0, 0.03336, 0.015], # Turkish
        "sv": [ 0.09383, 0.01535, 0.01486, 0.04702, 0.10149, 0.02027, 0.02862, 0.0209, 0.05817, 0.00614, 0.0314, 0.05275, 0.03471, 0.08542, 0.04482, 0.01839, 0.0002, 0.08431, 0.0659, 0.07691, 0.01919, 0.02415, 0.00142, 0.00159, 0.00708, 0.0007], # Swedish
        "pl": [ 0.10503, 0.0174, 0.03895, 0.03725, 0.07352, 0.00143, 0.01731, 0.01015, 0.08328, 0.01836, 0.02753, 0.02564, 0.02515, 0.06237, 0.06667, 0.02445, 0, 0.05243, 0.05224, 0.02475, 0.02062, 0.00012, 0.05813, 4e-005, 0.03206, 0.04852], # Polish
        "nl": [ 0.07486, 0.01584, 0.01242, 0.05933, 0.1891, 0.00805, 0.03403, 0.0238, 0.06499, 0.0146, 0.02248, 0.03568, 0.02213, 0.10032, 0.06063, 0.0157, 9e-005, 0.06411, 0.0373, 0.0679, 0.0199, 0.0285, 0.0152, 0.00036, 0.00035, 0.0139], # Dutch
        "da": [ 0.06025, 0.02, 0.00565, 0.05858, 0.15453, 0.02406, 0.04077, 0.01621, 0.06, 0.0073, 0.03395, 0.05229, 0.03237, 0.0724, 0.04636, 0.01756, 7e-005, 0.08956, 0.05805, 0.06862, 0.01979, 0.02332, 0.00069, 0.00028, 0.00698, 0.00034], # Danish
        "is": [ 0.1011, 0.01043, 0, 0.01575, 0.06418, 0.03013, 0.04241, 0.01871, 0.07578, 0.01144, 0.03314, 0.04532, 0.04041, 0.07711, 0.02166, 0.00789, 0, 0.08581, 0.0563, 0.04953, 0.04562, 0.02437, 0, 0.00046, 0.009, 0], # Icelandic
        "fi": [ 0.12217, 0.00281, 0.00281, 0.01043, 0.07968, 0.00194, 0.00392, 0.01851, 0.10817, 0.02042, 0.04973, 0.05761, 0.03202, 0.08826, 0.05614, 0.01842, 0.00013, 0.02872, 0.07862, 0.0875, 0.05008, 0.0225, 0.00094, 0.00031, 0.01745, 0.00051], # Finnish
        "cs": [ 0.08421, 0.00822, 0.0074, 0.03475, 0.07562, 0.00084, 0.00092, 0.01356, 0.06073, 0.01433, 0.02894, 0.03802, 0.02446, 0.06468, 0.06695, 0.01906, 1e-005, 0.04799, 0.05212, 0.05727, 0.0216, 0.05344, 0.00016, 0.00027, 0.01043, 0.01503], # Czech
        # Source: http://practicalcryptography.com/cryptanalysis/letter-frequencies-various-languages/
        "ru": [ 0.0804, 0.0155, 0.0475, 0.0188, 0.0295, 0.0821, 0.0022, 0.008, 0.0161, 0.0798, 0.0136, 0.0349, 0.0432, 0.0311, 0.0672, 0.1061, 0.0282, 0.0538, 0.0571, 0.0583, 0.0228, 0.0041, 0.0102, 0.0058, 0.0123, 0.0055, 0.0034, 0.0003, 0.0191, 0.0139, 0.0031, 0.0063, 0.02 ], # Russian
        # Source: https://everything2.com/title/Letter+frequency+in+several+languages
        "la": [ 0.072, 0.012, 0.033, 0.017, 0.092, 0.009, 0.014, 0.005, 0.101, 0, 0, 0.021, 0.034, 0.06, 0.044, 0.03, 0.013, 0.068, 0.068, 0.072, 0.074, 0.007, 0, 0.006, 0, 0 ], # Latin
    }

    alphabets = {
        "en": "ABCDEFGHIJKLMNOPQRSTUVWXYZ", # English
        "de": "ABCDEFGHIJKLMNOPQRSTUVWXYZÄÖÜß", # German
        "fr": "ABCDEFGHIJKLMNOPQRSTUVWXYZ", # French
        "es": "ABCDEFGHIJKLMNOPQRSTUVWXYZÑ", # Spanish
        "it": "ABCDEFGHIJKLMNOPQRSTUVWXYZ", # Italian
        "hu": "ABCDEFGHIJKLMNOPQRSTUVWXYZ", # Hungarian
        "ru": "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ", # Russian
        "cs": "ABCDEFGHIJKLMNOPQRSTUVWXYZ", # Slovak
        "la": "ABCDEFGHIJKLMNOPQRSTUVWXYZ", # Latin
        "el": "ΑΒΓΔΕΖΗΘΙΚΛΜΝΞΟΠΡΣΤΥΦΧΨΩ", # Greek
        "nl": "ABCDEFGHIJKLMNOPQRSTUVWXYZ", # Dutch
        "sv": "ABCDEFGHIJKLMNOPQRSTUVWXYZÅÄÖ", # Swedish
        "pt": "ABCDEFGHIJKLMNOPQRSTUVWXYZ", # Portuguese
        "pl": "AĄBCĆDEĘFGHIJKLŁMNŃOÓPQRSŚTUVWXYZŹŻ", # Polish
        "tr": "ABCÇDEFGĞHIİJKLMNOÖPRSŞTUÜVYZ", # Turkish
    }

    @staticmethod
    def language_code(language_id):
        """
        Retrieves the ISO language code for a given language ID.

        Parameters:
        - language_id (int): The index of the language in `supported_languages_codes`.

        Returns:
        - str: The language code, or an empty string if the index is invalid.
        """
        try:
            return LanguageStatistics.supported_languages_codes[language_id]
        except IndexError:
            return ""

    @staticmethod
    def language_id(language_code):
        """
        Retrieves the ID for a given language code.

        Parameters:
        - language_code (str): The language code.

        Returns:
        - int: The index of the language in `supported_languages_codes`.
        """
        return LanguageStatistics.supported_languages_codes.index(language_code.lower())

    @staticmethod
    def create_grams(language_code, language_statistics_directory, grams_type, use_spaces):
        """
        Creates a grams object of the specified type.

        Parameters:
        - language_code (str): The language code.
        - language_statistics_directory (str): Path to the language statistics directory.
        - grams_type (GramsType): The type of grams to create.
        - use_spaces (bool): Whether to include spaces in the analysis.

        Returns:
        - Grams: The created grams object.

        Raises:
        - ValueError: If the grams type is unsupported.
        """
        if grams_type == GramsType.Unigrams:
            return Unigrams(language_code, language_statistics_directory, use_spaces)
        elif grams_type == GramsType.Bigrams:
            return Bigrams(language_code, language_statistics_directory, use_spaces)
        elif grams_type == GramsType.Trigrams:
            return Trigrams(language_code, language_statistics_directory, use_spaces)
        elif grams_type == GramsType.Tetragrams:
            return Tetragrams(language_code, language_statistics_directory, use_spaces)
        elif grams_type == GramsType.Pentagrams:
            return Pentagrams(language_code, language_statistics_directory, use_spaces)
        elif grams_type == GramsType.Hexagrams:
            return Hexagrams(language_code, language_statistics_directory, use_spaces)
        else:
            raise ValueError(f"Unsupported grams type: {grams_type}")

    @staticmethod
    def create_grams_by_size(grams_size, language, language_statistics_directory, use_spaces=False):
        """
        Creates a grams object for the specified size (e.g., unigrams, bigrams, etc.).

        Parameters:
        - grams_size (int): The size of the grams to create (e.g., 1 for unigrams, 2 for bigrams).
        - language (str): The language code.
        - language_statistics_directory (str): Path to the language statistics directory.
        - use_spaces (bool): Whether to include spaces in the analysis (default: False).

        Returns:
        - Grams: The created grams object of the specified size.

        Raises:
        - ValueError: If the grams size is not supported.
        """
        grams_type = LanguageStatistics.get_grams_type_by_length(grams_size)
        return LanguageStatistics.create_grams(language, language_statistics_directory, grams_type, use_spaces)

    @staticmethod
    def get_grams_type_by_length(length):
        """
        Retrieves the GramsType corresponding to a specific length.

        Parameters:
        - length (int): The size of the grams (e.g., 1 for unigrams, 2 for bigrams).

        Returns:
        - GramsType: The corresponding GramsType for the given length.

        Raises:
        - ValueError: If the length does not correspond to a valid GramsType.
        """
        try:
            return GramsType(length)
        except ValueError:
            raise ValueError(f"No GramsType found for length: {length}")


    @staticmethod
    def alphabet(language, use_spaces=False):
        """
        Retrieves the alphabet for a given language.

        Parameters:
        - language (str): The language code.
        - use_spaces (bool): Whether to include spaces in the alphabet.

        Returns:
        - str: The alphabet for the language, or None if not found.
        """
        alphabet = LanguageStatistics.alphabets.get(language, None)
        if use_spaces and alphabet:
            return alphabet + " "
        return alphabet

    @staticmethod
    def calculate_ioc(plaintext):
        """
        Calculates the Index of Coincidence (IoC) for a given plaintext.

        Parameters:
        - plaintext (str): The input text.

        Returns:
        - float: The IoC of the text.
        """
        count_chars = {}
        for c in plaintext:
            count_chars[c] = count_chars.get(c, 0) + 1
        value = sum(cnt * (cnt - 1) for cnt in count_chars.values())
        N = len(plaintext)
        if N <= 1:
            return 0
        return value / (N * (N - 1))

    @staticmethod
    def map_numbers_into_text_space(numbers, alphabet, handling=HandlingOfUnknownSymbols.REMOVE, replace_character='?'):
        """
        Maps a list of numbers into text using a given alphabet.

        Parameters:
        - numbers (list): List of numbers to map.
        - alphabet (str): The alphabet for mapping.
        - handling (HandlingOfUnknownSymbols): How to handle unknown numbers.
        - replace_character (str): Replacement character for unknown numbers.

        Returns:
        - str: The resulting string.
        """
        string = ""
        if handling == HandlingOfUnknownSymbols.REMOVE:
            for n in numbers:
                if 0 <= n < len(alphabet):
                    string += alphabet[n]
        elif handling == HandlingOfUnknownSymbols.REPLACE:
            for n in numbers:
                if 0 <= n < len(alphabet):
                    string += alphabet[n]
                else:
                    string += replace_character
        else:
            raise ValueError(f"Invalid handling mode: {handling}")
        return string

    @staticmethod
    def map_text_into_number_space(text, alphabet, handling=HandlingOfUnknownSymbols.REMOVE, replace_number=-1):
        """
        Maps text into a list of numbers using a given alphabet.

        Parameters:
        - text (str): The input text.
        - alphabet (str): The alphabet for mapping.
        - handling (HandlingOfUnknownSymbols): How to handle unknown characters.
        - replace_number (int): Replacement number for unknown characters.

        Returns:
        - list: The resulting list of numbers.
        """
        numlist = []
        if handling == HandlingOfUnknownSymbols.REMOVE:
            for c in text:
                if c in alphabet:
                    numlist.append(alphabet.index(c))
        elif handling == HandlingOfUnknownSymbols.REPLACE:
            for c in text:
                if c in alphabet:
                    numlist.append(alphabet.index(c))
                else:
                    numlist.append(replace_number)
        else:
            raise ValueError(f"Invalid handling mode: {handling}")
        return numlist

    @staticmethod
    def load_word_tree(language_code, language_statistics_directory):
        """
        Loads a WordTree for a specific language.

        Parameters:
        - language_code (str): The language code.
        - language_statistics_directory (str): Path to the language statistics directory.

        Returns:
        - WordTree: The loaded WordTree object.
        """
        filename = os.path.join(language_statistics_directory, f"Dictionary_{language_code}.dic")
        with gzip.open(filename, 'rb') as filestream:
            return WordTree.deserialize(filestream)
