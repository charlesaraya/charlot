from functools import reduce
from enum import Enum
import re

from htmlnode import LeafNode, ParentNode

class TextType(Enum):
    NORMAL = "normal"
    ITALIC = "italic"
    BOLD = "bold"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"
    HORIZONTAL_RULE = "horizontal_rule"


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
            if len(text_split) == 1:
                new_nodes.append(node)
                continue
            for idx, text in enumerate(text_split):
                if not text:
                    continue
                if (idx+1) % 2 != 0:
                    new_nodes.append(TextNode(text, TextType.NORMAL))
                else:
                    new_nodes.append(TextNode(text, text_type))
    return new_nodes

URL_PATTERN = r"\[([^\]]+)\]\(((?:http[s]?:\/\/(?:[\w\-]+\.)+[\w-]+)?(?:\/[\S]*)*(?:\.\w+)?)\)"

def extract_markdown_images(text):
    matches = re.findall(r"!"+URL_PATTERN, text)
    return matches

def extract_markdown_links(text):
    matches = re.findall(URL_PATTERN, text)
    return matches

def split_nodes_image(old_nodes):
    new_nodes =[]
    for node in old_nodes:
        matches = extract_markdown_images(node.text)
        text = node.text
        if matches:
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
        else:
            new_nodes.append(node)
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes =[]
    for node in old_nodes:
        matches = extract_markdown_links(node.text)
        text = node.text
        if matches:
            for match in matches:
                alt_text, url = match
                delimiter = f"[{alt_text}]({url})"
                text = text.partition(delimiter)
                if text[0]:
                    new_nodes.append(TextNode(text[0], TextType.NORMAL))
                new_nodes.append(TextNode(alt_text, TextType.LINK, url))
                text = text[2]
            if text:
                new_nodes.append(TextNode(text, TextType.NORMAL))
        else:
            new_nodes.append(node)
    return new_nodes

def text_to_textnodes(text):
    initial_node = TextNode(text, TextType.NORMAL)
    nodes = [initial_node]

    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)

    delimiters_types = [("**", TextType.BOLD), ("_", TextType.ITALIC), ("`", TextType.CODE)]
    for delimiter, text_type in delimiters_types:
        try:
            nodes = split_nodes_delimiter(nodes, delimiter, text_type)
        except ValueError as e:
            print(f"Error {e}")
            continue
    return nodes

def markdown_to_blocks(markdown):
    markdown_blocks = markdown.split('\n\n')
    return list(map(lambda x: x.strip(), markdown_blocks))

def block_to_block_type(block):
    # Headings
    for i in range(1, 7):
        if block.startswith(f"{'#'*i} "):
            return BlockType.HEADING

    # Code Block
    lines = block.split('\n')
    if lines[0] == '```' and lines[-1] == '```':
        return BlockType.CODE

    # Quote Block, then Unordered list
    list_types = [('>', BlockType.QUOTE), ('-', BlockType.UNORDERED_LIST)]
    for list_type, block_type in list_types:
        if len(lines) == sum(list(map(lambda x: x.startswith(f"{list_type} "), lines))):
            return block_type

    # Horizontal Rule
    HR_REGEX = r"(^\*\*{1,}\*$)|(^--{1,}-$)|(^__{1,}_$)"
    match = re.match(HR_REGEX, block)
    if match:
        return BlockType.HORIZONTAL_RULE

    # Ordered List, otherwise is Paragraph
    for idx, line in enumerate(lines):
        if not line.startswith(f"{idx+1}. "):
            return BlockType.PARAGRAPH
    return BlockType.ORDERED_LIST

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    super_html_node = []
    for block in blocks:
        block_type = block_to_block_type(block)
        match block_type:
            case BlockType.PARAGRAPH:
                lines = block.split('\n')
                lines_of_text_nodes = list(map(text_to_textnodes, lines))
                html_p = generate_leafnodes_list(lines_of_text_nodes)
                html_p = list(map(lambda x: ParentNode('p', children=x), html_p))
                if len(html_p) > 1:
                    super_html_node.append(ParentNode('div', children=html_p))
                else:
                    super_html_node.append(html_p[0])
            case BlockType.HEADING:
                HEADING_PATTERN = r"^(#{1,6} )((?:\s*\w*)+)"
                matches = re.findall(HEADING_PATTERN, block)
                hastags, text = matches[0]
                num_hashtags = len(hastags) - 1 # w/o space
                html_h = LeafNode(f"h{num_hashtags}", text)
                super_html_node.append(html_h)
            case BlockType.CODE:
                lines = block.split('\n')
                text_lines = '\n'.join(lines[1:-1])
                super_html_node.append(ParentNode('pre', children=[ParentNode('code', children=[LeafNode(None, text_lines)])]))
            case BlockType.ORDERED_LIST | BlockType.UNORDERED_LIST:
                offset = 2 if block_type == BlockType.UNORDERED_LIST else 3
                lines = block.split('\n')
                text_lines = list(map(lambda x: x[offset:], lines))
                lines_of_text_nodes = list(map(text_to_textnodes, text_lines))
                html_p = generate_leafnodes_list(lines_of_text_nodes)
                html_p = list(map(lambda x: ParentNode('li', children=x), html_p))
                if block_type == BlockType.UNORDERED_LIST:
                    super_html_node.append(ParentNode('ul', children=html_p))
                else:
                    super_html_node.append(ParentNode('ol', children=html_p))
            case BlockType.QUOTE:
                lines = block.split('\n')
                text_lines = list(map(lambda x: x[2:], lines))
                quoted_text = reduce(lambda x, y: f"{x} {y}", text_lines, '').strip()
                lines_of_text_nodes = list(map(text_to_textnodes, [quoted_text]))
                html_p = generate_leafnodes_list(lines_of_text_nodes)
                super_html_node.append(ParentNode('blockquote', children=html_p[0]))
            case BlockType.HORIZONTAL_RULE:
                html_node = LeafNode('hr', None)
                super_html_node.append(html_node)
            case _:
                raise Exception(f"Markdown block type {block_type} not supported.")
    full_html = ParentNode('div', children=super_html_node)
    return full_html.to_html()

def inline_text_to_leaf(text_node):
    match text_node.text_type:
        case TextType.NORMAL:
            html_node = LeafNode(tag='', value=text_node.text)
        case TextType.BOLD:
            html_node = LeafNode('b', text_node.text)
        case TextType.ITALIC:
            html_node = LeafNode('i', text_node.text)
        case TextType.CODE:
            html_node = LeafNode('code', text_node.text)
        case TextType.LINK:
            html_node = LeafNode('a', text_node.text, {"href": text_node.url})
        case TextType.IMAGE:
            html_node = LeafNode('img', text_node.text, props={"src": text_node.url, "alt": text_node.text})
    return html_node

def generate_leafnodes_list(lines_of_text_nodes):
    leaf_nodes_list = []
    for text_nodes in lines_of_text_nodes:
        leaf_nodes = list(map(inline_text_to_leaf, text_nodes))
        leaf_nodes_list.append(leaf_nodes)
    return leaf_nodes_list

def extract_title(markdown):
    H1_PREFIX = '# '
    md_blocks = markdown_to_blocks(markdown)
    heading_md = list(filter(lambda x: x.startswith(H1_PREFIX), md_blocks))
    if heading_md:
        return heading_md[0].split(H1_PREFIX)[1]
    else:
        raise ValueError("No h1 markdown syntax found. Should start with '# '.", 1)

if __name__ == '__main__':
    link = "2023-10-27-functional-python.md"
    text = text = "**[Exploring the Depths of Functional Programming in Python](http://2023-10-27-functional-python.md/sdf/sdf.md)**:  A dive into Python's functional capabilities, beyond the usual list comprehensions. We'll explore `map`, `filter`, `reduce`, and more!"
    print(text_to_textnodes(text))
