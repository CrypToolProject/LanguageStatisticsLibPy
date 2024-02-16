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
from io import BufferedReader
from collections import deque
from Node import Node

class WordTree(Node):
    def __init__(self):
        super().__init__()
        self.stored_words = 0
        self.language_code = ''
        self.alphabet = ''

    @staticmethod
    def deserialize(reader: BufferedReader):
        tree = WordTree()

        # Load word tree header
        magic_no = reader.read(6).decode('utf-8')
        if magic_no != "CT2DIC":
            raise Exception("File does not start with the expected magic number for word tree.")
        
        # Read language code
        tree.language_code = ''
        char = reader.read(1).decode('utf-8')
        while char != '\0':
            tree.language_code += char
            char = reader.read(1).decode('utf-8')
        
        # Read alphabet
        tree.alphabet = ''
        char = reader.read(1).decode('utf-8')
        while char != '\0':
            tree.alphabet += char
            char = reader.read(1).decode('utf-8')
        
        # Read number of stored words
        tree.stored_words = int.from_bytes(reader.read(4), 'little')
        
        # Load word tree data structure
        stack = deque([tree])
        byte = reader.read(1)
        while byte:
            char = byte.decode('utf-8')
            if char == Node.WordEndSymbol:
                stack[-1].word_ends_here = True
                tree.stored_words += 1
            elif char == Node.TerminationSymbol:
                stack.pop()
            else:
                new_node = Node(char)
                stack[-1].child_nodes.append(new_node)
                stack.append(new_node)
            byte = reader.read(1)
        
        return tree

    def contains_word(self, word):
        word = word.upper()
        current_node = self
        for char in word:
            found_node = None
            for child_node in current_node.child_nodes:
                if child_node.value == char:
                    current_node = child_node
                    found_node = True
                    break
            if not found_node:
                return False
        return True

    def to_list(self):
        list_of_words = []
        stack = deque()
        
        def add_node_to_list(node, stack):
            stack.append(node.value)
            if node.word_ends_here:
                list_of_words.append(''.join(stack))
            for child_node in node.child_nodes:
                add_node_to_list(child_node, deque(stack))
            stack.pop()
        
        for node in self.child_nodes:
            add_node_to_list(node, stack)
        
        return list_of_words