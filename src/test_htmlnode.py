import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_with_multiple_props(self):
        #test that props are converted correctly where there are multiple props
        node = HTMLNode(props={"href": "https://www.google.com", "target": "_blank"})
        self.assertEqual(node.props_to_html(), ' href="https://www.google.com" target="_blank"')
    
    def test_props_to_html_with_one_prop(self):
        #test with just one prop
        node = HTMLNode(props={"class": "button"})
        self.assertEqual(node.props_to_html(), ' class="button"')

    def test_props_to_html_with_no_props(self):
        #test with no props
        node = HTMLNode()
        self.assertEqual(node.props_to_html(), "")

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "I love boys")
        self.assertEqual(node.to_html(), "<p>I love boys</p>")

    def test_leaf_to_html_h1(self):
        node = LeafNode("h1", "I love code")
        self.assertEqual(node.to_html(), "<h1>I love code</h1>")
    
    def test_leaf_to_html_h2(self):
        node = LeafNode("h2", "I love skateboard")
        self.assertEqual(node.to_html(), "<h2>I love skateboard</h2>")
    
    def test_leaf_to_html_a(self):
        node = LeafNode("a", "3rd Lair", props={"href": "https://www.3rdLair.com", "target": "_blank"})
        self.assertEqual(node.to_html(), '<a href="https://www.3rdLair.com" target="_blank">3rd Lair</a>')


    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )
    
    def test_nested_parent_nodes(self):
        inner_leaf = LeafNode("span", "I am deeply nested")
        inner_parent = ParentNode("div", [inner_leaf])
        middle_parent = ParentNode("section", [inner_parent])
        outer_parent = ParentNode("article", [
            LeafNode("h1", "My Article Title"),
            middle_parent, 
            LeafNode("footer", "Copyright 2023")
        ])
        expected_html = "<article><h1>My Article Title</h1><section><div><span>I am deeply nested</span></div></section><footer>Copyright 2023</footer></article>"

        self.assertEqual(outer_parent.to_html(), expected_html)

if __name__ == "__main__":
    unittest.main()