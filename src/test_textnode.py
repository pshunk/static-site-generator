import unittest
from textnode import TextNode, TextType, text_node_to_html_node, text_type_from_delimiter, split_nodes_delimiter,\
extract_markdown_links, extract_markdown_images, split_nodes_image, split_nodes_link, text_to_text_nodes


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

    def test_bold_delimiter(self):
        self.assertEqual(text_type_from_delimiter("**"), TextType.BOLD)

    def test_code_delimiter(self):
            self.assertEqual(text_type_from_delimiter("`"), TextType.CODE)

    def test_split_nodes(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`")
        self.assertEqual(new_nodes, [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ])

    def test_split_nodes_bold(self):
        node = TextNode("This is text with a **bold** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**")
        self.assertEqual(new_nodes, [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" word", TextType.TEXT),
        ])

    def test_split_nodes_bold_end_of_sentence(self):
        node = TextNode("This is text with a bold **word**", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**")
        self.assertEqual(new_nodes, [
            TextNode("This is text with a bold ", TextType.TEXT),
            TextNode("word", TextType.BOLD),
        ])

    def test_split_nodes_bold_beginning_of_sentence(self):
            node = TextNode("**This** is text with a bold word", TextType.TEXT)
            new_nodes = split_nodes_delimiter([node], "**")
            self.assertEqual(new_nodes, [
                TextNode("This", TextType.BOLD),
                TextNode(" is text with a bold word", TextType.TEXT),
            ])

    def test_split_nodes_text_only(self):
        node = TextNode("This is text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`")
        self.assertEqual(new_nodes, [TextNode("This is text", TextType.TEXT)])

    def test_split_nodes_bold_and_bold(self):
        node = TextNode("This is **text** with two **bold** words", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**")
        self.assertEqual(new_nodes, [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with two ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" words", TextType.TEXT),
        ])

    def test_split_nodes_bold_and_italic(self):
        node = TextNode("This is text with **bold** and _italic_ words", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_")
        self.assertEqual(new_nodes, [
            TextNode("This is text with **bold** and ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" words", TextType.TEXT),
        ])

    def test_split_nodes_multiple_nodes(self):
        node_1 = TextNode("This is text with a **bold** word", TextType.TEXT)
        node_2 = TextNode("This **is** text with a bold word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node_1, node_2], "**")
        self.assertEqual(new_nodes, [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" word", TextType.TEXT),
            TextNode("This ", TextType.TEXT),
            TextNode("is", TextType.BOLD),
            TextNode(" text with a bold word", TextType.TEXT)
        ])

    def test_split_nodes_bold_type(self):
        node = TextNode("bold text", TextType.BOLD)
        new_nodes = split_nodes_delimiter([node], "**")
        self.assertEqual(new_nodes, [TextNode("bold text", TextType.BOLD)])

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a link [to google](https://www.google.com) and [to youtube](https://www.youtube.com)"
        )
        self.assertListEqual(matches, [("to google", "https://www.google.com"), ("to youtube", "https://www.youtube.com")])

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )

    def test_split_images_beginning_of_sentence(self):
        node = TextNode(
            "![This](https://i.imgur.com/zjjcJKZ.png) is text with an image and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" is text with an image and another ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://i.imgur.com/zjjcJKZ.png) and another [second link](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second link", TextType.LINK, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )

    def test_split_links_beginning_of_sentence(self):
        node = TextNode(
            "[This](https://i.imgur.com/zjjcJKZ.png) is text with a link and another [second link](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" is text with a link and another ", TextType.TEXT),
                TextNode("second link", TextType.LINK, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )

    def test_split_images_plain_text(self):
        node = TextNode("plain text", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([TextNode("plain text", TextType.TEXT)], new_nodes)

    def test_split_links_plain_text(self):
        node = TextNode("plain text", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([TextNode("plain text", TextType.TEXT)], new_nodes)

    def test_split_images_multiple_nodes(self):
        node_1 = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        node_2 = TextNode(
            "![This](https://i.imgur.com/zjjcJKZ.png) is text with an image and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT
        )
        new_nodes = split_nodes_image([node_1, node_2])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
                TextNode("This", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" is text with an image and another ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )

    def test_split_links_multiple_nodes(self):
        node_1 = TextNode(
            "This is text with a [link](https://i.imgur.com/zjjcJKZ.png) and another [second link](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        node_2 = TextNode(
            "[This](https://i.imgur.com/zjjcJKZ.png) is text with a link and another [second link](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT
        )
        new_nodes = split_nodes_link([node_1, node_2])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second link", TextType.LINK, "https://i.imgur.com/3elNhQu.png"),
                TextNode("This", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" is text with a link and another ", TextType.TEXT),
                TextNode("second link", TextType.LINK, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )

    def test_text_to_text_nodes(self):
        nodes = text_to_text_nodes("text")
        self.assertListEqual([TextNode("text", TextType.TEXT)], nodes)

    def test_text_to_text_nodes_bold(self):
        nodes = text_to_text_nodes("**text**")
        self.assertListEqual([TextNode("text", TextType.BOLD)], nodes)

    def test_text_to_text_nodes_everything(self):
        nodes = text_to_text_nodes("This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](www.google.com)")
        self.assertListEqual(nodes, [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "www.google.com"),
        ])

if __name__ == "__main__":
    unittest.main()