class HTMLNode:
    def __init__(self, tag: str = None, value: str = None, children: list = None, props: dict = None):
        self.tag =tag
        self.value = value
        self.children = children
        self.props = props

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        if self.props:
            return ''.join(list(map(lambda key: f' {key}="{self.props[key]}"', self.props)))
        return ''
