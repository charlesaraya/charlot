class HTMLNode:
    def __init__(self, tag: str = None, value: str = None, children: list = None, props: dict = None):
        self.tag =tag
        self.value = value
        self.children = children
        self.props = props

    def __repr__(self):
        return f"{self.__class__.__name__}({self.tag}, {self.value}, {self.children}, {self.props})"

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        if self.props:
            return ''.join(list(map(lambda key: f' {key}="{self.props[key]}"', self.props)))
        return ''

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if not self.tag:
            return self.value
        if self.tag and not self.value:
            return f"<{self.tag}{self.props_to_html()}>"
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if not self.tag:
            raise ValueError("A parent node must have a tag")
        if not self.children:
            raise ValueError("A parent node must have children nodes")

        return f"<{self.tag}{self.props_to_html()}>{''.join(map(lambda x: x.to_html(), self.children))}</{self.tag}>"
