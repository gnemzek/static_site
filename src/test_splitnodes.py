import unittest
from textnode import TextNode, TextType
from split_nodes import split_nodes_delimiter

class TestSplitNodesDelimiter(unittest.TestCase):
    def test_bold_delimiter(self):
        # Test with bold delimiter "**"
        node = TextNode("This is text with a **bolded phrase** in the middle", TextType.text)
        new_nodes = split_nodes_delimiter([node], "**", TextType.bold)

        # Check that we got 3 nodes
        self.assertEqual(len(new_nodes), 3)

        # Check the content and type of each node
        self.assertEqual(new_nodes[0].text, "This is text with a ")
        self.assertEqual(new_nodes[0].text_type, TextType.text)
        
        self.assertEqual(new_nodes[1].text, "bolded phrase")
        self.assertEqual(new_nodes[1].text_type, TextType.bold)
        
        self.assertEqual(new_nodes[2].text, " in the middle")
        self.assertEqual(new_nodes[2].text_type, TextType.text)

    def test_italic_delimiter(self):
        # Test with italic delimiter "_"
        node = TextNode("This is text with a _italic phrase_ in the middle", TextType.text)
        new_nodes = split_nodes_delimiter([node], "_", TextType.italic)

        # Check that we got 3 nodes
        self.assertEqual(len(new_nodes), 3)

        # Check the content and type of each node
        self.assertEqual(new_nodes[0].text, "This is text with a ")
        self.assertEqual(new_nodes[0].text_type, TextType.text)
        
        self.assertEqual(new_nodes[1].text, "italic phrase")
        self.assertEqual(new_nodes[1].text_type, TextType.italic)
        
        self.assertEqual(new_nodes[2].text, " in the middle")
        self.assertEqual(new_nodes[2].text_type, TextType.text)

    
    def test_code_delimiter(self):
        # Test with code delimiter "_"
        node = TextNode("This is text with a `code block` in the middle", TextType.text)
        new_nodes = split_nodes_delimiter([node], "`", TextType.code)

        # Check that we got 3 nodes
        self.assertEqual(len(new_nodes), 3)

        # Check the content and type of each node
        self.assertEqual(new_nodes[0].text, "This is text with a ")
        self.assertEqual(new_nodes[0].text_type, TextType.text)
        
        self.assertEqual(new_nodes[1].text, "code block")
        self.assertEqual(new_nodes[1].text_type, TextType.code)
        
        self.assertEqual(new_nodes[2].text, " in the middle")
        self.assertEqual(new_nodes[2].text_type, TextType.text)