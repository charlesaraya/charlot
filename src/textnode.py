from enum import Enum
import re

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

def split_nodes_image(old_nodes):
    new_nodes =[]
    for node in old_nodes:
        matches = extract_markdown_images(node.text)
        text = node.text
        for match in matches:
            alt_text, url = match
            delimiter = f"![{alt_text}]({url})"
            text = text.partition(delimiter)
            if text[0]:
                new_nodes.append(TextNode(text[0], TextType.NORMAL))
            new_nodes.append(TextNode(alt_text, TextType.IMAGE, url))
            text = text[2]
        if text:
            new_nodes.append(TextNode(text, TextType.NORMAL))
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes =[]
    for node in old_nodes:
        matches = extract_markdown_links(node.text)
        text = node.text
        for match in matches:
            alt_text, url = match
            delimiter = f"![{alt_text}]({url})"
            text = text.partition(delimiter)
            if text[0]:
                new_nodes.append(TextNode(text[0], TextType.NORMAL))
            new_nodes.append(TextNode(alt_text, TextType.LINK, url))
            text = text[2]
        if text:
            new_nodes.append(TextNode(text, TextType.NORMAL))
    return new_nodes

URL_PATTERN = r"\[(\w+(?:\s*\w*)*)\]\((http(?:s)?:\/\/[\w]+\.[\S]+\.\w+(?:[A-Za-z0-9-\._~!\$&'\*\+,;=:@\/\?])*)\)"

def extract_markdown_images(text):
    matches = re.findall(r"!"+URL_PATTERN, text)
    return matches

def extract_markdown_links(text):
    matches = re.findall(URL_PATTERN, text)
    return matches

if __name__ == '__main__':
    text_node_with_images = TextNode("![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg) the end", TextType.NORMAL)
    #text_with_links = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
    new_nodes = split_nodes_image([text_node_with_images])
    print(new_nodes)
