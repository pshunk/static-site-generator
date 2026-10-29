import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode
# from textnode import TextType, text_to_text_nodes


class TestHTMLNode(unittest.TestCase):
    def test_props_eq(self):
        node = HTMLNode(
            props={
                "href": "https://www.google.com",
                "target": "_blank",
            })
        self.assertEqual(node.props_to_html(), ' href="https://www.google.com" target="_blank"')

    def test_empty(self):
        node = HTMLNode()
        self.assertEqual(node.props_to_html(), "")

    def test_full_node(self):
        node = HTMLNode("p", "this is a paragraph", [HTMLNode()],
            props={
                "href": "https://www.google.com",
                "target": "_blank",
            })
        self.assertEqual(node.props_to_html(), ' href="https://www.google.com" target="_blank"')

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')

    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")

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

    def test_to_html_with_multiple_children(self):
        child_1 = LeafNode("b", "Bold text")
        child_2 = LeafNode(None, "Normal text")
        child_3 = LeafNode("i", "italic text")
        child_4 = LeafNode(None, "Normal text")
        parent_node = ParentNode("p", [child_1, child_2, child_3, child_4])
        self.assertEqual(parent_node.to_html(), "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>")

if __name__ == "__main__":
    unittest.main()