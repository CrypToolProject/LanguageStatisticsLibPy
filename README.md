# LanguageStatisticsLibPy

The LanguageStatisticsLibPy is a Python library designed to facilitate the fast analysis and manipulation of language statistics data. It was first used in the widespread cryptography e-learning software CrypTool 2. 

The library supports 15 different languages and offers functionality for generating and handling n-gram data, specifically for calculating n-gram frequencies using the language statistics files from CrypTool 2. 
Additionally, it facilitates the use of CrypTool 2's dictionaries through a "Word Tree", an efficient data structure for rapid word searches within a language.

The language statistics files (for example, `en-5gram-nocs.gz` indicates an English 5-gram file that is not case-sensitive and excludes spaces) can be found in the "LanguageStatistics" subdirectory of CrypTool 2, if you have installed CrypTool 2 on Windows.
If you don't have a Windows machine or you don't want to install CrypTool 2, you may download the language statistics files and dictionaries from the CrypTool 2 Github repo: [Language Statistics](https://github.com/CrypToolProject/CrypTool-2/tree/main/LanguageStatistics).

Remark: This package contains the implemented algorithms without the language statistics files. These files have to be downloaded separately as they occupy around xxx MB.

## Features

- **Support for Multiple Languages**: The library includes predefined support for fifteen languages, including English, German, Spanish, French, each with its own set of unigram frequencies and alphabets.
  
- **N-Gram Loading**: Users can load unigrams, bigrams, trigrams, tetragrams, pentagrams, and hexagrams as n-gram objects in supported languages, with the option to include or exclude spaces. The n-grams delivered in the language statistics files range from 1 to 5. All language statistics files delivered are case-insensitive, denoted as "nocs" in the filename. Each language statistics is available in two forms: with space/blank ("sp" in the filename) and without space/blank (indicated by the absence of "sp" in the filename) within the alphabet.

- **Index of Coincidence Calculation**: It offers a method to calculate the index of coincidence (IoC) for a given plaintext, which is useful for cryptanalysis and language pattern recognition.
  
- **Alphabet and Number Mapping**: The library provides functionality to map characters to their respective positions in a language's alphabet and vice versa, supporting operations on encoded messages or language data.

- **Dynamic N-Gram and Word Tree Support**: Depending on the available data, the library dynamically supports various n-gram types and can load a word tree structure for efficient word lookups in a specific language.

## Usage

1. **Initialization**: Start by importing the `LanguageStatistics` class and specify the language code for your analysis.
2. **Loading N-Grams**: To load n-grams of your chosen type (e.g., unigrams, bigrams) for a specific language, use the `create_grams` method with the appropriate .gz file from the LanguageStatistics directory in CrypTool 2. For instance, to load English 4-grams that are case-insensitive and include the space/blank symbol, use the file named `en-4gram-nocs-sp.gz`.
3. **Calculating IoC**: Calculate the index of coincidence for a given plaintext using the `calculate_ioc` method.
4. **Word Tree Loading**: For advanced language analysis, load a pre-built word tree for a specific language using the `load_word_tree` method.

Sample usage:

```python
from xxxxxx.LanguageStatistics import LanguageStatistics

plaintext = LanguageStatistics.map_text_into_number_space("HALLOWELT", LanguageStatistics.alphabets['de'])
ioc = LanguageStatistics.calculate_ioc(plaintext)

print(ioc)
```

You can find further example usages in the file `Test.py` within the package.

## Supported Languages

The library includes predefined configurations for the following languages:
- English (en)
- German (de)
- Spanish (es)
- French (fr)
- Italian (it)
- Hungarian (hu)
- Russian (ru)
- Czech (cs)
- Greek (el)
- Latin (la)
- Dutch (nl)
- Swedish (sv)
- Portuguese (pt)
- Polish (pl)
- Turkish (tr)
