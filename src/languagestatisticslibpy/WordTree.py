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
from io import BufferedReader
from collections import deque
from languagestatisticslibpy.Node import Node

class WordTree(Node):
    """
    Represents a tree data structure for storing words and efficiently querying them.

    Inherits:
    - Node: The base class for tree nodes, where each node represents a character.

    Attributes:
    - stored_words (int): The number of words stored in the tree.
    - language_code (str): The language code for the words stored in the tree.
    - alphabet (str): The alphabet used in the stored words.
    """

    def __init__(self):
        """
        Initializes an empty WordTree.

        Initializes:
        - stored_words (int): Set to 0, as no words are initially stored.
        - language_code (str): Empty, to be set during deserialization.
        - alphabet (str): Empty, to be set during deserialization.
        """
        super().__init__()
        self.stored_words = 0
        self.language_code = ''
        self.alphabet = ''

    @staticmethod
    def deserialize(reader: BufferedReader):
        """
        Deserializes a WordTree from a binary file.

        Parameters:
        - reader (BufferedReader): A binary file reader containing the serialized WordTree.

        Returns:
        - WordTree: The deserialized WordTree object.

        Raises:
        - Exception: If the file format is invalid or the magic number does not match.

        Process:
        1. Reads the file header and validates the magic number.
        2. Reads the language code and alphabet.
        3. Reads the number of stored words.
        4. Constructs the WordTree structure by iterating through the file's serialized data.
        """
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
        """
        Checks whether a given word exists in the WordTree.

        Parameters:
        - word (str): The word to search for.

        Returns:
        - bool: True if the word exists in the tree, False otherwise.

        Process:
        1. Converts the word to uppercase for case-insensitive comparison.
        2. Traverses the tree to find the sequence of characters in the word.
        3. Returns False if any character is missing in the tree structure.
        """
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
        """
        Converts all words stored in the WordTree into a list.

        Returns:
        - list: A list of all words stored in the tree.

        Process:
        1. Traverses the tree using a stack to collect characters.
        2. Adds a word to the list whenever a node marks the end of a word.
        """
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