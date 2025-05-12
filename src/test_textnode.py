import unittest

from textnode import TextNode, TextType, text_node_to_html_node
from split_nodes import *
from textnode import *


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.bold)
        node2 = TextNode("This is a text node", TextType.bold)
        self.assertEqual(node, node2)

    def test_noteq(self):
        node = TextNode("This is a text node", TextType.bold)
        node2 = TextNode("This is a text node", TextType.text)
        self.assertNotEqual(node, node2)

    def test_noteq2(self):
        node = TextNode("Foo", TextType.bold, "www.ccs.com")
        node2 = TextNode("Foo", TextType.bold)
        self.assertNotEqual(node, node2)

    def test_text(self):
        node = TextNode("This is a text node", TextType.text)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("This is a text node", TextType.bold)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a text node")

    def test_italic(self):
        node = TextNode("This is a text node", TextType.italic)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is a text node")

    def test_code(self):
        node = TextNode("This is a text node", TextType.code)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a text node")

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.text,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.text),
                TextNode("image", TextType.image,
                         "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.text),
                TextNode(
                    "second image", TextType.image, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with a link to [3rd Lair](https://www.3rdlair.com) and another to [ccs](https://www.ccs.com)",
            TextType.text,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a link to ", TextType.text),
                TextNode("3rd Lair", TextType.link, "https://www.3rdlair.com"),
                TextNode(" and another to ", TextType.text),
                TextNode(
                    "ccs", TextType.link, "https://www.ccs.com"
                ),
            ],
            new_nodes,
        )

    def test_split_images_no_images(self):
        # Create a node with just regular text (no images)
        node = TextNode(
            "This is just regular text with no images in it.",
            TextType.text,
        )

        # Call the split_nodes_image function
        new_nodes = split_nodes_image([node])

        # Since there are no images, the function should return the original node
        self.assertListEqual(
            [
                TextNode(
                    "This is just regular text with no images in it.", TextType.text),
            ],
            new_nodes,
        )

    def test_split_links_no_links(self):
        # Create a node with just regular text (no links)
        node = TextNode(
            "This is just regular text with no links in it.",
            TextType.text,
        )

        # Call the split_nodes_link function
        new_nodes = split_nodes_link([node])

        # Since there are no links, the function should return the original node
        self.assertListEqual(
            [
                TextNode(
                    "This is just regular text with no links in it.", TextType.text),
            ],
            new_nodes,
        )

    def test_text_to_textnodes_all(self):
        node = TextNode(
            "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)", TextType.text,
        )

        # call function to split nodes
        new_nodes = text_to_textnodes(node.text)

        self.assertListEqual(
            [
                TextNode("This is ", TextType.text),
                TextNode("text", TextType.bold),
                TextNode(" with an ", TextType.text),
                TextNode("italic", TextType.italic),
                TextNode(" word and a ", TextType.text),
                TextNode("code block", TextType.code),
                TextNode(" and an ", TextType.text),
                TextNode("obi wan image", TextType.image,
                         "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.text),
                TextNode("link", TextType.link, "https://boot.dev"),
            ],
            new_nodes
        )

    def test_text_to_textnodes_none(self):
        node = TextNode(
            "This is just regular text", TextType.text,
        )

        # call function to split nodes
        new_nodes = text_to_textnodes(node.text)

        self.assertListEqual(
            [
                TextNode("This is just regular text", TextType.text)
            ],
            new_nodes
        )


if __name__ == "__main__":
    unittest.main()
