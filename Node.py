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
class Node:
    WordEndSymbol = chr(1)  # Constant for the symbol indicating the end of a word
    TerminationSymbol = chr(0)  # Constant for the symbol indicating the end of the tree

    def __init__(self, value=None):
        self.value = value  # The value of this node
        self.word_ends_here = False  # Indicator if a word ends at this node
        self.child_nodes = []  # All child nodes of this node

    def __eq__(self, other):
        if not isinstance(other, Node):
            return False
        if self.value != other.value or self.word_ends_here != other.word_ends_here:
            return False
        if len(self.child_nodes) != len(other.child_nodes):
            return False
        for i in range(len(self.child_nodes)):
            if self.child_nodes[i] != other.child_nodes[i]:
                return False
        return True

    def __hash__(self):
        # Calculate a hash value for this node
        hash_value = hash(self.value)
        hash_value = hash_value * 31 + hash(self.word_ends_here)
        for child_node in self.child_nodes:
            hash_value = hash_value * 31 + hash(child_node)
        return hash_value