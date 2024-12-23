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
from enum import Enum

class GramsType(Enum):
    Undefined = 0       # invalid type
    Unigrams = 1        # 1-grams
    Bigrams = 2         # 2-grams
    Trigrams = 3        # 3-grams
    Tetragrams = 4      # 4-grams
    Pentagrams = 5     # 5-grams
    Hexagrams = 6       # 6-grams