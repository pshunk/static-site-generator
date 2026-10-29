import unittest
from functions import markdown_to_blocks, block_to_block_type, BlockType, block_to_text, get_parent, markdown_to_html_node
from htmlnode import LeafNode, ParentNode


class TestFunctions(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_block_to_block_type_paragraph(self):
        self.assertEqual(block_to_block_type("This is a paragraph"), BlockType.PARAGRAPH)

    def test_block_to_block_type_heading(self):
        self.assertEqual(block_to_block_type("# This is a heading"), BlockType.HEADING)

    def test_block_to_block_type_not_heading(self):
        self.assertEqual(block_to_block_type("###########This should not be a heading"), BlockType.PARAGRAPH)

    def test_block_to_block_type_code(self):
        self.assertEqual(block_to_block_type(
            "```\nThis is a code block\n```"
        ), BlockType.CODE)

    def test_block_to_block_type_not_code(self):
        self.assertEqual(block_to_block_type(
            "```\nThis should not be a code block\n"
        ), BlockType.PARAGRAPH)

    def test_block_to_block_type_quote(self):
        self.assertEqual(block_to_block_type(">This\n> is\n>a\n> quote"), BlockType.QUOTE)

    def test_block_to_block_type_not_quote(self):
        self.assertEqual(block_to_block_type(">This\n> is\n<NOT\n>a\n> quote"), BlockType.PARAGRAPH)

    def test_block_to_block_type_unordered(self):
        self.assertEqual(block_to_block_type("- This\n- is\n- an\n- unordered\n- list"), BlockType.UNORDERED_LIST)

    def test_block_to_block_type_not_unordered(self):
        self.assertEqual(block_to_block_type("- This\n- is\n-NOT\n- an\n- unordered\n- list"), BlockType.PARAGRAPH)

    def test_block_to_block_type_ordered(self):
        self.assertEqual(block_to_block_type("1. This\n2. is\n3. an\n4. ordered\n5. list"), BlockType.ORDERED_LIST)

    def test_block_to_block_type_not_ordered(self):
        self.assertEqual(block_to_block_type("1. This\n2. is\n69. NOT\n3. an\n4. ordered\n5. list"), BlockType.PARAGRAPH)

    def test_block_to_text(self):
        self.assertEqual(block_to_text("This is a paragraph", BlockType.PARAGRAPH), "This is a paragraph")

    def test_block_to_text_heading(self):
        self.assertEqual(block_to_text("### This is a heading", BlockType.HEADING), "This is a heading")

    def test_block_to_text_code(self):
        self.assertEqual(block_to_text("```\nThis is code\n```", BlockType.CODE), "This is code")

    def test_block_to_text_quote(self):
        self.assertEqual(block_to_text("> This\n>is\n> a\n>quote", BlockType.QUOTE), "This\nis\na\nquote")

    def test_block_to_text_unordered(self):
        self.assertEqual(block_to_text("- This\n- is\n- an\n- unordered list", BlockType.UNORDERED_LIST), "This\nis\nan\nunordered list")

    def test_block_to_text_ordered(self):
        self.assertEqual(block_to_text("1. This is\n2. an ordered list", BlockType.ORDERED_LIST), "This is\nan ordered list")

    def test_get_parent_paragraph(self):
        parent = get_parent("This is a paragraph")
        self.assertEqual(parent, ParentNode("p", [LeafNode(None, "This is a paragraph")]))

    def test_get_parent_heading(self):
        parent = get_parent("# This is a heading")
        self.assertEqual(parent, ParentNode("h1", [LeafNode(None, "This is a heading")]))

    def test_get_parent_code(self):
        parent = get_parent("```\nThis is code\n```")
        self.assertEqual(parent, ParentNode("pre", [LeafNode("code", "This is code")]))

    def test_get_parent_quote(self):
        parent = get_parent("> This is\n> a quote")
        self.assertEqual(parent, ParentNode("blockquote", [LeafNode(None, "This is"), LeafNode(None, "a quote")]))

    def test_get_parent_unordered(self):
        parent = get_parent("- This is\n- an unordered list")
        self.assertEqual(parent, ParentNode("ul", [ParentNode("li", [LeafNode(None, "This is")]), ParentNode("li", [LeafNode(None, "an unordered list")])]))

    def test_get_parent_ordered(self):
        parent = get_parent("1. This is\n2. an ordered list")
        self.assertEqual(parent, ParentNode("ol", [ParentNode("li", [LeafNode(None, "This is")]), ParentNode("li", [LeafNode(None, "an ordered list")])]))



    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )



    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff</code></pre></div>",
        )

if __name__ == "__main__":
    unittest.main()