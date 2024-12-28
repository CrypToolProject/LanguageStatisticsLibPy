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
from enum import Enum

class GramsType(Enum):
    """
    Enum representing the types of n-grams.

    Attributes:
    - Undefined (int): Represents an invalid or uninitialized type (value: 0).
    - Unigrams (int): Represents 1-grams, single characters (value: 1).
    - Bigrams (int): Represents 2-grams, pairs of characters (value: 2).
    - Trigrams (int): Represents 3-grams, triplets of characters (value: 3).
    - Tetragrams (int): Represents 4-grams, quadruplets of characters (value: 4).
    - Pentagrams (int): Represents 5-grams, quintuplets of characters (value: 5).
    - Hexagrams (int): Represents 6-grams, sextuplets of characters (value: 6).
    """

    Undefined = 0       # Invalid or uninitialized type
    Unigrams = 1        # 1-grams (single characters)
    Bigrams = 2         # 2-grams (pairs of characters)
    Trigrams = 3        # 3-grams (triplets of characters)
    Tetragrams = 4      # 4-grams (quadruplets of characters)
    Pentagrams = 5      # 5-grams (quintuplets of characters)
    Hexagrams = 6       # 6-grams (sextuplets of characters)