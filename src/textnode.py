import re
from enum import Enum
from htmlnode import LeafNode

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode:

    def __init__(self, text: str, text_type: TextType, url: str | None = None) -> None:
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other: TextNode) -> bool:
        return self.text == other.text and self.text_type == other.text_type and self.url == other.url

    def __repr__(self) -> str:
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"

def text_node_to_html_node(text_node: TextNode) -> LeafNode:
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})

def text_type_from_delimiter(delimiter: str) -> TextType:
    match delimiter:
        case "**":
            return TextType.BOLD
        case "_":
            return TextType.ITALIC
        case "`":
            return TextType.CODE
        case _:
            raise Exception("Error: delimiter does not correspond to text type")

def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str) -> list[TextNode]:
    nodes: list[TextNode] = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            nodes.append(node)
        else:
            split_text = node.text.split(delimiter)
            if len(split_text) % 2 != 1:
                raise Exception("Error: invalid markdown syntax")
            for i in range(len(split_text)):
                if split_text[i] != "":
                    nodes.append(TextNode(split_text[i], TextType.TEXT if i%2 == 0 else text_type_from_delimiter(delimiter)))
    return nodes

def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    nodes: list[TextNode] = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            nodes.append(node)
        else:
            images = extract_markdown_images(node.text)
            if len(images) == 0:
                nodes.append(node)
            current_nodes: list[TextNode] = []
            for alt_text, url in images:
                split_text = []
                if len(current_nodes) == 0:
                    split_text = node.text.split(f"![{alt_text}]({url})", 1)
                else:
                    split_text = current_nodes.pop().text.split(f"![{alt_text}]({url})", 1)
                if split_text[0] != "":
                    current_nodes.append(TextNode(split_text[0], TextType.TEXT))
                current_nodes.append(TextNode(alt_text, TextType.IMAGE, url))
                if split_text[1] != "":
                    current_nodes.append(TextNode(split_text[1], TextType.TEXT))
            nodes.extend(current_nodes)
    return nodes

def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    nodes: list[TextNode] = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            nodes.append(node)
        else:
            links = extract_markdown_links(node.text)
            if len(links) == 0:
                nodes.append(node)
            current_nodes: list[TextNode] = []
            for anchor_text, url in links:
                split_text = []
                if len(current_nodes) == 0:
                    split_text = node.text.split(f"[{anchor_text}]({url})", 1)
                else:
                    split_text = current_nodes.pop().text.split(f"[{anchor_text}]({url})", 1)
                if split_text[0] != "":
                    current_nodes.append(TextNode(split_text[0], TextType.TEXT))
                current_nodes.append(TextNode(anchor_text, TextType.LINK, url))
                if split_text[1] != "":
                    current_nodes.append(TextNode(split_text[1], TextType.TEXT))
            nodes.extend(current_nodes)
    return nodes

def text_to_text_nodes(text: str) -> list[TextNode]:
    node = TextNode(text, TextType.TEXT)
    nodes = split_nodes_delimiter([node], "**")
    nodes = split_nodes_delimiter(nodes, "_")
    nodes = split_nodes_delimiter(nodes, "`")
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes