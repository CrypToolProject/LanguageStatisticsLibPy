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
from languagestatisticslibpy.LanguageStatistics import LanguageStatistics
from datetime import datetime

# Change this path to the folder where the CrypTool-2 language statistics are stored, 
# e.g. the folder "LanguageStatistics" in the standard CrypTool-2 installation folder.
# You need to have CrypTool 2 installed to run this test or at least the CrypTool 2 
# language statistics and dictionary files all in the same folder somewhere on your computer
ct2_language_statistics_folder = "C:\\Program Files\\CrypTool 2\\LanguageStatistics"

# test the cost calculation of all gram classes except hexagrams
for i in range(1, 6):

    #write current ngam size
    print("Grams size:", i)

    #load grams for English
    start = datetime.now()
    grams = LanguageStatistics.create_grams_by_size(i, "en", ct2_language_statistics_folder, False)
    print("\tGrams loaded in", (datetime.now() - start))

    #normalize the grams
    start = datetime.now()
    grams.normalize(1000000.0)
    print("\tGrams normalized in", (datetime.now() - start))

    # we map the text into the number space of the grams
    numbers = LanguageStatistics.map_text_into_number_space("HELLOWORLDTHISISATEST", grams.alphabet)

    #calculate the cost of the text
    cost = grams.calculate_cost(numbers)

    #convert the numbers back into the text space
    text = LanguageStatistics.map_numbers_into_text_space(numbers, grams.alphabet)
    print("\tText:", text)

    #print the cost
    print("\tCost value:", cost)

#test the word tree
print("Loading word tree")
start = datetime.now()
tree = LanguageStatistics.load_word_tree("en", ct2_language_statistics_folder)
print("\tWord tree loaded", (datetime.now() - start))
print("\tTotal number of words in tree", tree.stored_words)

word = "Hello"
print("Word:", word)
print("\tContains word:", tree.contains_word(word))

word = "World"
print("Word:", word)
print("\tContains word:", tree.contains_word(word))

word = "HelloWorld"
print("Word:", word)
print("\tContains word:", tree.contains_word(word))
