from enum import Enum

from htmlnode import LeafNode

class TextType(Enum):
    NORMAL = "normal"
    ITALIC = "italic"
    BOLD = "bold"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"


class TextNode:
    def __init__(self, text, text_type, url = None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, text_node):
        return (self.text == text_node.text 
                and self.text_type == text_node.text_type
                and self.url == text_node.url)

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"

def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.NORMAL:
            return LeafNode(None, text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
        case _:
            raise Exception(f"Node's text type {text_node.text_type} not supported.")

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    if (delimiter == '**' and text_type is not TextType.BOLD
        or delimiter == '_' and text_type is not TextType.ITALIC
        or delimiter == '`' and text_type is not TextType.CODE):
        raise ValueError(f"Delimiter {delimiter} does not match {text_type}.")

    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.NORMAL:
            new_nodes.append(node)
        else:
            text_split = node.text.split(delimiter)
            if len(text_split) in [1, 2]:
                raise ValueError(f"Delimiter/s {delimiter} not found")
            for idx, text in enumerate(text_split):
                if (idx+1) % 2 != 0:
                    new_nodes.append(TextNode(text, TextType.NORMAL))
                else:
                    new_nodes.append(TextNode(text, text_type))
    return new_nodes

if __name__ == '__main__':
    bold_node = TextNode("**important notice**", TextType.BOLD)
    link_node = TextNode("[link](https://www.example.com)", TextType.LINK)
    img_node = TextNode("![alt text for image](url/of/image.jpg)", TextType.IMAGE)
    bold_node_1 = TextNode("This is **text** with a `code block` word", TextType.NORMAL)
    bold_node_2 = TextNode("And this is more **important** with a **bold text** word", TextType.NORMAL)
    new_nodes = split_nodes_delimiter([bold_node, bold_node_1, link_node, img_node, bold_node_2], "**", TextType.BOLD)
    print(new_nodes)
