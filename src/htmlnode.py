class HTMLNode:
    def __init__(self, tag: str = None, value: str = None, children: list = None, props: dict = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("to_html method not implemented")

    def props_to_html(self) -> str:
        if not self.props:
            return ""
        
        attributes = []
        for key, value in self.props.items():
            attributes.append(f' {key}="{value}"')
            
        return "".join(attributes)

    def __repr__(self) -> str:
        return f"HTMLNode(tag={self.tag}, value={self.value}, children={self.children}, props={self.props})"

class LeafNode(HTMLNode):
    def __init__(self, tag: str, value: str, props: dict = None):
        # Leaf nodes cannot have children, so we explicitly pass None to the parent
        super().__init__(tag=tag, value=value, children=None, props=props)

    def to_html(self) -> str:
        if self.value is None:
            raise ValueError("All leaf nodes must have a value")
        
        # If there's no tag, render the value as raw text
        if self.tag is None:
            return self.value
            
        # Wrap the value inside the HTML opening and closing tags
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

class ParentNode(HTMLNode):
    def __init__(self, tag: str, children: list, props: dict = None):
        # Parent nodes must have a tag and children, but no direct text value
        super().__init__(tag=tag, value=None, children=children, props=props)

    def to_html(self) -> str:
        if self.tag is None:
            raise ValueError("ParentNode must have a tag")
        if self.children is None:
            raise ValueError("ParentNode must have children")
        
        # Recursively render all child nodes into an HTML string
        children_html = ""
        for child in self.children:
            children_html += child.to_html()
            
        # Wrap everything inside the parent's opening and closing tags
        return f"<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>"