# LanguageStatisticsLibPy

LanguageStatisticsLibPy is a Python library designed to facilitate the fast analysis and manipulation of language statistics data. It originates from a C# library that was first used in the widespread cryptography e-learning software CrypTool 2. From now on "CrypTool 2" is abbreviated "CT2". CT2 is an open-source e-learning program for Windows to do cryptography and cryptanalysis (https://www.cryptool.org/en/ct2/).

This Python library supports 15 different languages and offers functionality for generating and handling n-gram data, specifically for calculating n-gram frequencies using the language statistics files from CT2.
Additionally, it facilitates the use of CT2's dictionaries through a "Word Tree", an efficient data structure for rapid word searches within a language.

The language statistics files (for example, `en-5gram-nocs.gz` indicates an English 5-gram file that is not case-sensitive and excludes spaces) can be found in the "LanguageStatistics" subdirectory of CT2, if you have installed CT2 on Windows.
If you don't have a Windows machine or you don't want to install CT2, you may download the language statistics files and dictionaries from the CT2 Github repo: [Language Statistics](https://github.com/CrypToolProject/CrypTool-2/tree/main/LanguageStatistics).

Remark: This package contains the implemented algorithms without the language statistics files. These files have to be downloaded separately as they occupy many megabytes.

## Features

- **Support for multiple languages**: The library includes predefined support for 15 languages, including English, German, Spanish, French -- each with its own set of unigram frequencies and alphabets.
  
- **N-gram loading**: Users can load unigrams, bigrams, trigrams, tetragrams, pentagrams, and hexagrams as n-gram objects in supported languages, with the option to include or exclude spaces. The n-grams delivered in the language statistics files range from 1 to 5 (we don't deliver 6-grams within CT2, since these files are too big). All language statistics files delivered are case-insensitive, denoted as "nocs" in the filename. Each language statistics is available in two forms: with space/blank ("sp" in the filename) and without space/blank (indicated by the absence of "sp" in the filename) within the alphabet.

- **Index of Coincidence calculation**: It offers a method to calculate the index of coincidence (IoC) for a given plaintext, which is useful for cryptanalysis and language pattern recognition.
  
- **Alphabet and number mapping**: The library provides functionality to map characters to their respective positions in a language's alphabet and vice versa, supporting operations on encoded messages or language data.

- **Dynamic n-gram support**: Depending on the available data, the library dynamically supports various n-gram types. 
- **Word tree data structure**: It supports a word tree data structure for fast word lookups (true = part of language, false = not part of language) of a specific language.

## Usage

Prerequisites: LanguageStatisticsLibPy is installed on your computer via 
**$ pip3 install LanguageStatisticsLibPy**

1. **Initialization**: Start by importing the `LanguageStatistics` class and specify the language code for your analysis.
2. **Loading n-grams**: To load n-grams of your chosen type (e.g., unigrams, bigrams) for a specific language, use the `create_grams` method with the appropriate .gz file from the LanguageStatistics directory in CT2. For instance, to load English 4-grams that are case-insensitive and include the space/blank symbol, use the file named `en-4gram-nocs-sp.gz`.
3. **Calculating IoC**: Calculate the index of coincidence for a given plaintext using the `calculate_ioc` method.
4. **Word tree loading**: For advanced language analysis, load a pre-built word tree for a specific language using the `load_word_tree` method.

Sample usage (from file `test1.py`):

```python
from languagestatisticslibpy.LanguageStatistics import LanguageStatistics as LS

plaintext = LS.map_text_into_number_space("HELLOWORD", LS.alphabets['en'])
ioc = LS.calculate_ioc(plaintext)

print(ioc)
```

You can find further example usages in the file `test2.py` within the package.

## Supported languages

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


## Some more technical details

### Where are the package files stored after installing the package and how to find this out

```bash
% pip3 list | grep  LanguageStatisticsLibPy
% pip3 show  LanguageStatisticsLibPy

# show package content (including the test files) for example on Mac
% tree /Users/be/Library/Python/3.13/lib/python/site-packages/LanguageStatisticsLibPy
# on Linux this could be in:
# /home/user/.local/lib/python3.10/site-packages/LanguageStatisticsLibPy/
...
# show content of a directory where the statistics files had been copied to
tree /Users/be/Documents/Python/LanguageStatisticsLibPy_PIP-Test/LSLP
...
```

### How to call the test files
```bash
% pwd
/Users/be/Documents/Python/LanguageStatisticsLibPy_PIP-Test/testen2

% ls -l
-rwx------  1 be  staff   956 27 Dez 09:44 test1.py
-rwx------  1 be  staff  2944 27 Dez 09:42 test2.py

% python3 test1.py                                                     
0.08333333333333333

% python3 test2.py
Grams size: 1
	Grams loaded in 0:00:00.000097
	Grams normalized in 0:00:00.000007
	Text: HELLOWORLDTHISISATEST
	Cost value: 771793.56
...
```