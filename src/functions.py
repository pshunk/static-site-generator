from enum import Enum
from htmlnode import HTMLNode, LeafNode, ParentNode
from textnode import TextType, TextNode, text_to_text_nodes, text_node_to_html_node

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def markdown_to_blocks(markdown: str) -> list[str]:
    blocks = markdown.split("\n\n")
    stripped_blocks = []
    for block in blocks:
        if block.strip() != "":
            stripped_blocks.append(block.strip())
    return stripped_blocks

def block_to_block_type(block: str) -> BlockType:
    head = block.split(" ")[0]
    if head.count("#") == len(head) and len(head) <= 6:
        return BlockType.HEADING
    lines = block.split("\n")
    if lines[0] == "```" and lines[-1] == "```":
        return BlockType.CODE
    for i in range(len(lines)):
        if not lines[i].startswith(">"):
            break
        if i == len(lines) - 1:
            return BlockType.QUOTE
    for i in range(len(lines)):
        if not lines[i].startswith("- "):
            break
        if i == len(lines) - 1:
            return BlockType.UNORDERED_LIST
    for i in range(1, len(lines) + 1):
        if not lines[i - 1].startswith(f"{i}. "):
            break
        if i == len(lines):
            return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH

def markdown_to_html_node(markdown: str) -> HTMLNode:
    children = []
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        children.append(get_parent(block))
    return ParentNode("div", children)

def get_parent(block: str) -> HTMLNode:
    type = block_to_block_type(block)
    text = block_to_text(block, type)
    match type:
        case BlockType.PARAGRAPH:
            leaf_nodes = []
            paragraph_text = text.replace("\n", " ")
            text_nodes = text_to_text_nodes(paragraph_text)
            for text_node in text_nodes:
                leaf_nodes.append(text_node_to_html_node(text_node))
            return ParentNode("p", leaf_nodes)
        case BlockType.HEADING:
            leaf_nodes = []
            text_nodes = text_to_text_nodes(text)
            for text_node in text_nodes:
                leaf_nodes.append(text_node_to_html_node(text_node))
            heading_number = len(block.split(" ")[0])
            tag = f"h{heading_number}"
            return ParentNode(tag, leaf_nodes)
        case BlockType.CODE:
            leaf = LeafNode("code", text)
            return ParentNode("pre", [leaf])
        case BlockType.QUOTE:
            leaf_nodes = []
            replaced_text = text.replace("\n", "<br>")
            text_nodes = text_to_text_nodes(replaced_text)
            for text_node in text_nodes:
                leaf_nodes.append(text_node_to_html_node(text_node))
            return ParentNode("blockquote", leaf_nodes)
        case BlockType.UNORDERED_LIST:
            lines = text.split("\n")
            parent_nodes = []
            for line in lines:
                leaf_nodes = []
                text_nodes = text_to_text_nodes(line)
                for text_node in text_nodes:
                    leaf_nodes.append(text_node_to_html_node(text_node))
                parent_nodes.append(ParentNode("li", leaf_nodes))
            return ParentNode("ul", parent_nodes)
        case BlockType.ORDERED_LIST:
            lines = text.split("\n")
            parent_nodes = []
            for line in lines:
                leaf_nodes = []
                text_nodes = text_to_text_nodes(line)
                for text_node in text_nodes:
                    leaf_nodes.append(text_node_to_html_node(text_node))
                parent_nodes.append(ParentNode("li", leaf_nodes))
            return ParentNode("ol", parent_nodes)

def block_to_text(block: str, type: BlockType) -> str:
    match type:
        case BlockType.PARAGRAPH:
            return block
        case BlockType.HEADING:
            return " ".join(block.split(" ")[1:])
        case BlockType.CODE:
            return "\n".join(block.split("\n")[1:-1])
        case BlockType.QUOTE:
            return "\n".join(list(map(lambda x:
                            "" if len(x) < 3 else x[2:] if x[1] == " " else x[1:],
                            block.split("\n"))))
        case BlockType.UNORDERED_LIST:
            return "\n".join(list(map(lambda x: "" if len(x) < 3 else x[2:], block.split("\n"))))
        case BlockType.ORDERED_LIST:
            return "\n".join(list(map(lambda x: " ".join(x.split(" ")[1:]), block.split("\n"))))