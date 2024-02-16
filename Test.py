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
from LanguageStatistics import LanguageStatistics
from datetime import datetime

ct2_folder = "C:\\Users\\nilsk\\Desktop\\CrypTool-2_git\\CrypTool-2"

# test the cost calculation of all gram classes except hexagrams
for i in range(1, 6):

    #write current ngam size
    print("Grams size:", i)

    #load grams for English
    start = datetime.now()
    grams = LanguageStatistics.create_grams_by_size(i, "en", ct2_folder + "\\LanguageStatistics", False)
    print("Grams loaded in ", (datetime.now() - start))

    #normalize the grams
    start = datetime.now()
    grams.normalize(1000000.0)
    print("Grams normalized in ", (datetime.now() - start))

    # we map the text into the number space of the grams
    numbers = LanguageStatistics.map_text_into_number_space("HELLOWORLDTHISISATEST", grams.alphabet)

    #calculate the cost of the text
    cost = grams.calculate_cost(numbers)

    #convert the numbers back into the text space
    text = LanguageStatistics.map_numbers_into_text_space(numbers, grams.alphabet)
    print("Text:", text)

    #print the cost
    print("Cost value:", cost)

#test the word tree
print("Loading word tree")
tree = LanguageStatistics.load_word_tree("en", ct2_folder + "\\LanguageStatistics")
print("Word tree loaded")

word = "Hello"
print("Word:", word)
print("Contains word:", tree.contains_word(word))

word = "World"
print("Word:", word)
print("Contains word:", tree.contains_word(word))

word = "HelloWorld"
print("Word:", word)
print("Contains word:", tree.contains_word(word))