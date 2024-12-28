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

class Node:
    """
    Represents a single node in a tree structure for storing characters.

    Attributes:
    - WordEndSymbol (str): A constant indicating the end of a word in the tree (default: `chr(1)`).
    - TerminationSymbol (str): A constant indicating the end of a tree branch (default: `chr(0)`).
    - value (str or None): The character or value stored in this node.
    - word_ends_here (bool): Whether this node marks the end of a word.
    - child_nodes (list): A list of child nodes connected to this node.
    """

    WordEndSymbol = chr(1)  # Constant for the symbol indicating the end of a word
    TerminationSymbol = chr(0)  # Constant for the symbol indicating the end of the tree

    def __init__(self, value=None):
        """
        Initializes a Node object.

        Parameters:
        - value (str or None): The character or value to be stored in this node (default: None).

        Initializes:
        - self.value (str or None): The value of this node.
        - self.word_ends_here (bool): Set to False initially, indicating that no word ends here.
        - self.child_nodes (list): An empty list to hold child nodes.
        """
        self.value = value
        self.word_ends_here = False
        self.child_nodes = []

    def __eq__(self, other):
        """
        Compares two Node objects for equality.

        Parameters:
        - other (Node): The node to compare with.

        Returns:
        - bool: True if both nodes are equal, False otherwise.

        Notes:
        - Two nodes are considered equal if:
          - Their values are the same.
          - Their `word_ends_here` flags are the same.
          - Their child nodes are identical in value and order.
        """
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
        """
        Calculates a hash value for the Node.

        Returns:
        - int: A hash value based on the node's value, `word_ends_here` status, and child nodes.

        Notes:
        - This method allows the node to be used in hash-based collections (e.g., sets, dictionaries).
        """
        hash_value = hash(self.value)
        hash_value = hash_value * 31 + hash(self.word_ends_here)
        for child_node in self.child_nodes:
            hash_value = hash_value * 31 + hash(child_node)
        return hash_value
