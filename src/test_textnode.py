import unittest
from textnode import TextNode, TextType, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_not_eq(self):
            node = TextNode("This is a text node", TextType.BOLD)
            node2 = TextNode("This is also a text node", TextType.BOLD)
            self.assertNotEqual(node, node2)

    def test_eq_again(self):
            node = TextNode("This is a text node", TextType.BOLD, "www.com")
            node2 = TextNode("This is a text node", TextType.BOLD, "www.com")
            self.assertEqual(node, node2)

    def test_not_eq_again(self):
            node = TextNode("This is a text node", TextType.BOLD)
            node2 = TextNode("This is a text node", TextType.BOLD, "www.com")
            self.assertNotEqual(node, node2)

    def test_not_eq_again_again(self):
            node = TextNode("This is a text node", TextType.BOLD)
            node2 = TextNode("This is a text node", TextType.ITALIC)
            self.assertNotEqual(node, node2)

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
            node = TextNode("This is a bold node", TextType.BOLD)
            html_node = text_node_to_html_node(node)
            self.assertEqual(html_node.tag, "b")
            self.assertEqual(html_node.value, "This is a bold node")

    def test_link(self):
            node = TextNode("This is a link node", TextType.LINK, "www.com")
            html_node = text_node_to_html_node(node)
            self.assertEqual(html_node.tag, "a")
            self.assertEqual(html_node.value, "This is a link node")
            self.assertDictEqual(html_node.props, {"href": "www.com"})

    def test_img(self):
                node = TextNode("This is an image node", TextType.IMAGE, "www.com")
                html_node = text_node_to_html_node(node)
                self.assertEqual(html_node.tag, "img")
                self.assertEqual(html_node.value, "")
                self.assertDictEqual(html_node.props, {"src": "www.com", "alt": "This is an image node"})


if __name__ == "__main__":
    unittest.main()