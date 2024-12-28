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

   Usage: python3 test1.py
   test1.py is a minimal working example (MWE) which just needs the
   package LanguageStatisticsLibPy to be installed.
'''

from languagestatisticslibpy.LanguageStatistics import LanguageStatistics as LS

plaintext = LS.map_text_into_number_space("HELLOWORD", LS.alphabets['en'])
ioc = LS.calculate_ioc(plaintext)

print(ioc)
