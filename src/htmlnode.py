

class HTMLNode:
    
    def __init__(self, tag: str | None = None, value: str | None = None, children: list[HTMLNode] | None = None, props: dict[str, str] | None = None) -> None:
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self) -> str:
        raise NotImplementedError("Error: to_html must be implemented in child class")

    def props_to_html(self) -> str:
        string = ""
        if self.props is None or len(self.props) == 0:
            return string
        for key in self.props:
            string += f' {key}="{self.props[key]}"'
        return string

    def __eq__(self, other: HTMLNode) -> bool:
        return self.tag == other.tag and self.value == other.value and self.children == other.children and self.props == other.props

    def __repr__(self) -> str:
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"

class LeafNode(HTMLNode):

    def __init__(self, tag: str | None, value: str | None, props: dict[str, str] | None = None) -> None:
        super().__init__(tag, value, None, props)

    def to_html(self) -> str:
        if self.value is None:
            raise ValueError("Error: node must have a value")
        if self.tag is None:
            return self.value
        if self.props is None:
            return f"<{self.tag}>{self.value}</{self.tag}>"
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    def __repr__(self) -> str:
        return f"LeafNode({self.tag}, {self.value}, {self.props})"

class ParentNode(HTMLNode):

    def __init__(self, tag: str | None, children: list[HTMLNode] | None, props: dict[str, str] | None = None) -> None:
        super().__init__(tag, None, children, props)

    def to_html(self) -> str:
        if self.tag is None:
            raise ValueError("Error: node must have a tag")
        if self.children is None:
            raise ValueError("Error: parent node has no children")
        string = ""
        for child in self.children:
            string += child.to_html()
        return f"<{self.tag}>{string}</{self.tag}>"

