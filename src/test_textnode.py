import unittest

from textnode import (
    TextNode,
    TextType,
    text_node_to_html_node,
    split_nodes_delimiter,
    extract_images,
    extract_links,
    extract_emails,
    split_nodes,
    text_to_textnodes,
    markdown_to_blocks,
    BlockType,
    block_to_block_type,
    markdown_to_html_node,
    extract_title,
)

class TestTextNode(unittest.TestCase):
    empty_node = TextNode("", TextType.NORMAL)
    normal_node = TextNode("This is a text node", TextType.NORMAL)
    bold_node = TextNode("This is a test node", TextType.BOLD)
    same_bold_node = TextNode("This is a test node", TextType.BOLD)
    same_bold_node_and_link = TextNode("This is a test node", TextType.BOLD, "https://charlot.dev")
    diff_bold_node = TextNode("This is a different test node", TextType.BOLD)
    link_node = TextNode("Click here!", TextType.LINK, "https://example.com")

    def test_eq(self):
        self.assertEqual(TestTextNode.bold_node, TestTextNode.same_bold_node)
        self.assertNotEqual(TestTextNode.bold_node, TestTextNode.diff_bold_node)
        self.assertNotEqual(TestTextNode.bold_node, TestTextNode.same_bold_node_and_link)
        self.assertNotEqual(TestTextNode.bold_node, TestTextNode.link_node)
        self.assertEqual(TestTextNode.bold_node.url, None)
    
    def test_node_to_html(self):
        normal_html_node = text_node_to_html_node(TestTextNode.normal_node)
        self.assertEqual(normal_html_node.tag, None)
        self.assertEqual(normal_html_node.value, "This is a text node")

        link_html_node = text_node_to_html_node(TestTextNode.link_node)
        self.assertEqual(link_html_node.tag, "a")
        self.assertEqual(link_html_node.value, 'Click here!')
        self.assertEqual(link_html_node.props, {"href": "https://example.com"})

        # A TextNode of type TextType.BOLD and url is converted to a LeafNode w/o props
        not_link_html_node = text_node_to_html_node(TestTextNode.same_bold_node_and_link)
        self.assertEqual(not_link_html_node.tag, "b")
        self.assertEqual(not_link_html_node.props, None)

    def test_split_nodes_delimiter(self):

        bold = TextNode("This is important information", TextType.BOLD)
        no_split = split_nodes_delimiter([bold], "**", TextType.BOLD)
        self.assertEqual(no_split[0], bold)

        text_bold = TextNode("Click the **'Submit'** button to proceed.", TextType.NORMAL)
        bold_split = split_nodes_delimiter([text_bold], "**", TextType.BOLD)
        self.assertEqual(bold_split[1].text, "'Submit'")

        text_italics = TextNode("Check some _fancy italics_", TextType.NORMAL)
        italic_split = split_nodes_delimiter([text_italics], "_", TextType.ITALIC)
        self.assertEqual(italic_split[1].text, "fancy italics")

        text_code = TextNode('Use `git commit -m "Your message"` to save changes', TextType.NORMAL)
        code_split = split_nodes_delimiter([text_code], "`", TextType.CODE)
        self.assertEqual(code_split[1].text, 'git commit -m "Your message"')

        text_double_bold = TextNode("**Warning**: This action **cannot** be undone!", TextType.NORMAL)
        double_split = split_nodes_delimiter([text_double_bold], "**", TextType.BOLD)
        self.assertEqual(double_split[0].text, "Warning")
        self.assertEqual(double_split[2].text, "cannot")

    def test_extract_markdown_images(self):
        text_with_images = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        expected_result = [("rick roll", "https://i.imgur.com/aKaOqIh.gif", "![rick roll](https://i.imgur.com/aKaOqIh.gif)"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg", "![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)")]
        matches = extract_images(text_with_images)
        self.assertListEqual(matches, expected_result)

    def test_extract_markdown_links(self):
        bad_links = [
            "[link](asd)",
            "[link](http::)",
            "[link](http::)",
            "[link](http: //example.com)",
            "[link](http://example)",
            "[li]nk](http://example)",
        ]
        expected_result = [[]]*len(bad_links)
        result = list(map(extract_links, bad_links))
        self.assertListEqual(result, expected_result)

        good_links = [
            ("[link](http://google.com)", ("link", "http://google.com", "[link](http://google.com)")),
            ("[link](http://google.com)", ("link", "http://google.com", "[link](http://google.com)")),
            ("[a link](http://google.com)", ("a link", "http://google.com", "[a link](http://google.com)")),
            ("[google.com](http://google.com)", ("google.com", "http://google.com", "[google.com](http://google.com)")),
            ("[A 'fancy' link](http://google.com)", ("A 'fancy' link", "http://google.com", "[A 'fancy' link](http://google.com)")),
            ("[rel link](/google.com)", ("rel link", "/google.com", "[rel link](/google.com)")),
            ("[link](http://www.google.com)", ("link", "http://www.google.com", "[link](http://www.google.com)")),
            ("[link](http://www.google.com/)", ("link", "http://www.google.com/", "[link](http://www.google.com/)")),
            ("[link](http://www.google.com/asd)", ("link", "http://www.google.com/asd", "[link](http://www.google.com/asd)")),
            ("[link](http://www.google.com/a-sd/)", ("link", "http://www.google.com/a-sd/", "[link](http://www.google.com/a-sd/)")),
            ("[link](http://www.google.com/asd/cat.jpeg)", ("link", "http://www.google.com/asd/cat.jpeg", "[link](http://www.google.com/asd/cat.jpeg)")),
            ("[link](http://www.google.com/asd/@cat.jpeg)", ("link", "http://www.google.com/asd/@cat.jpeg", "[link](http://www.google.com/asd/@cat.jpeg)")),
        ]
        links = [link[0] for link in good_links]
        expected_result = [[link[1]] for link in good_links]
        result = list(map(extract_links, links))
        self.assertListEqual(result, expected_result)

        multiple_links = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        expected_result = [("to boot dev", "https://www.boot.dev", "[to boot dev](https://www.boot.dev)"), ("to youtube", "https://www.youtube.com/@bootdotdev", "[to youtube](https://www.youtube.com/@bootdotdev)")]
        self.assertListEqual(extract_links(multiple_links), expected_result)

    def test_extract_markdown_emails(self):
        good_emails = "This is text with a <john.doe@gmail.com> and <foo.bar_baz@companyx.co.uk>."
        expected_result = [("john.doe@gmail.com", "mailto:john.doe@gmail.com", "<john.doe@gmail.com>"), ("foo.bar_baz@companyx.co.uk", "mailto:foo.bar_baz@companyx.co.uk", "<foo.bar_baz@companyx.co.uk>")]
        matches = extract_emails(good_emails)
        self.assertListEqual(matches, expected_result)

    def test_split_nodes_image(self):
        self.assertEqual(split_nodes([TestTextNode.empty_node], extract_images, TextType.IMAGE), [TestTextNode.empty_node])
        self.assertEqual(split_nodes([TestTextNode.normal_node], extract_images, TextType.IMAGE), [TestTextNode.normal_node])

        start_text = TextNode("Check ", TextType.NORMAL)
        image1 = TextNode("rick roll", TextType.IMAGE, "https://i.imgur.com/aKaOqIh.gif")
        mid_text = TextNode(" and ", TextType.NORMAL)
        image2 = TextNode("obi wan", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg")
        end_text = TextNode(" and enjoy", TextType.NORMAL)

        between_text_node = TextNode("Check ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg) and enjoy", TextType.NORMAL)
        expected_result = [start_text, image1, mid_text, image2, end_text]
        self.assertListEqual(split_nodes([between_text_node], extract_images, TextType.IMAGE), expected_result)

        start_image_node = TextNode("![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg) and enjoy", TextType.NORMAL)
        expected_result = [image1, mid_text, image2, end_text]
        self.assertListEqual(split_nodes([start_image_node], extract_images, TextType.IMAGE), expected_result)

        end_image_node = TextNode("Check ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)", TextType.NORMAL)
        expected_result = [start_text, image1, mid_text, image2]
        self.assertListEqual(split_nodes([end_image_node], extract_images, TextType.IMAGE), expected_result)

    def test_split_nodes_link(self):
        self.assertEqual(split_nodes([TestTextNode.empty_node], extract_links, TextType.LINK), [TestTextNode.empty_node])
        self.assertEqual(split_nodes([TestTextNode.normal_node], extract_links, TextType.LINK), [TestTextNode.normal_node])

        start_text = TextNode("This is text with a link ", TextType.NORMAL)
        link1 = TextNode("to boot dev", TextType.LINK, "https://www.boot.dev")
        mid_text = TextNode(" and ", TextType.NORMAL)
        link2 = TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev")
        end_text = TextNode(", enjoy!", TextType.NORMAL)

        between_text_node = TextNode("This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev), enjoy!", TextType.NORMAL)
        expected_result = [start_text, link1, mid_text, link2, end_text]
        self.assertListEqual(split_nodes([between_text_node], extract_links, TextType.LINK), expected_result)

        start_link_node = TextNode("[to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev), enjoy!", TextType.NORMAL)
        expected_result = [link1, mid_text, link2, end_text]
        self.assertListEqual(split_nodes([start_link_node], extract_links, TextType.LINK), expected_result)

        end_link_node = TextNode("This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)", TextType.NORMAL)
        expected_result = [start_text, link1, mid_text, link2]
        self.assertListEqual(split_nodes([end_link_node], extract_links, TextType.LINK), expected_result)

    def test_split_nodes_email(self):
        start_text = TextNode("This is text with a ", TextType.NORMAL)
        link1 = TextNode("john.doe@gmail.com", TextType.EMAIL, "mailto:john.doe@gmail.com")
        mid_text = TextNode(" and ", TextType.NORMAL)
        link2 = TextNode("foo.bar_baz@companyx.co.uk", TextType.EMAIL, "mailto:foo.bar_baz@companyx.co.uk")
        end_text = TextNode(".", TextType.NORMAL)

        good_emails = TextNode("This is text with a <john.doe@gmail.com> and <foo.bar_baz@companyx.co.uk>.", TextType.NORMAL)
        expected_result = [start_text, link1, mid_text, link2, end_text]
        splitted_nodes = split_nodes([good_emails], extract_emails, TextType.EMAIL)
        self.assertListEqual(splitted_nodes, expected_result)

    def test_text_to_textnodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and **specially** a [link](https://boot.dev). Clear!"
        expected_result = [
            TextNode("This is ", TextType.NORMAL),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.NORMAL),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.NORMAL),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.NORMAL),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and ", TextType.NORMAL),
            TextNode("specially", TextType.BOLD),
            TextNode(" a ", TextType.NORMAL),
            TextNode("link", TextType.LINK, "https://boot.dev"),
            TextNode(". Clear!", TextType.NORMAL)
        ]
        self.assertListEqual(text_to_textnodes(text), expected_result)

    def test_markdown_to_blocks(self):
        md = """This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        expected_result = [
            "This is **bolded** paragraph",
            "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
            "- This is a list\n- with items",
        ]
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, expected_result)

    def test_capture_heading(self):
        good_headings = """# Heading 1

## Heading 2

### Heading 3

####  Heading 4

#####  Heading 5

######  Heading 6

Heading 1
======

Heading 2
-----

# Heading 1
======

# Heading 2
-----

Heading 1
======

Heading 2 -
-----
"""
        blocks = markdown_to_blocks(good_headings)
        expected_result = [BlockType.HEADING] * len(blocks)
        block_types = [block_to_block_type(block) for block in blocks]
        self.assertListEqual(block_types, expected_result)

        bad_headings ="""

#######  Normal text because more than 6 heading

Heading 1
=

Heading 2
-
"""
        blocks = markdown_to_blocks(bad_headings)
        expected_result = [BlockType.PARAGRAPH] * len(blocks)
        block_types = [block_to_block_type(block) for block in blocks]
        self.assertNotEqual(block_types, bad_headings)

    def test_block_to_block_type(self):
        md = """# Heading 1

This is a paragraph of text. It has some **bold** and _italic_ words inside of it.

- This is the first list item in a list block
- This is a list item
- This is another list item

### Heading 3

> This is the first list item in a list block
> This is a list item
> This is another list item

---

######  Heading 6

```
This is the first list item in a list block
This is a list item
This is another list item
```

#######  Normal text because more than 6 heading

___

Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam sed sodales dolor, quis ultricies est.

1. This is the first list item in a list block
2. This is a list item
3. This is another list item

___f

Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam sed sodales dolor, quis ultricies est.
"""
        expected_result = [
            BlockType.HEADING,
            BlockType.PARAGRAPH,
            BlockType.UNORDERED_LIST,
            BlockType.HEADING,
            BlockType.QUOTE,
            BlockType.HORIZONTAL_RULE,
            BlockType.HEADING,
            BlockType.CODE,
            BlockType.PARAGRAPH,
            BlockType.HORIZONTAL_RULE,
            BlockType.PARAGRAPH,
            BlockType.ORDERED_LIST,
            BlockType.PARAGRAPH,
            BlockType.PARAGRAPH,
        ]
        blocks = markdown_to_blocks(md)
        block_types = [block_to_block_type(block) for block in blocks]
        self.assertEqual(block_types, expected_result)

    def test_markdown_to_html_node(self):
        markdown = """\n# Heading 1\n\n## Heading 2\n\n### Heading 3\n\n#### Heading 4\n\n##### Heading 5\n\n###### Heading 6\n\n####### Not a heading 7\n\nParagraph with **bold** and _italic_ and [a link](https://example.com) and [an image](https://example.com/asd/cat.jpg).\nThat also has a right **edge bold**\n`git commit -m "Yeah"` to commit.\n\n----\n\n- An unordered list.\n- **This** is a _list item_\n- This [cat](https://example.com) rocks\n\n> Do or do not. \n> There is no try.\n\n```\ndef say_hello():\n    print("Hello world!")\n    \nsay_hello()\n```\n\n****\n\n1. An ordered list.\n2. **This** is a _list item_\n3. This [cat](https://example.com) rocks\n"""
        expected_result = """<div><h1>Heading 1</h1><h2>Heading 2</h2><h3>Heading 3</h3><h4>Heading 4</h4><h5>Heading 5</h5><h6>Heading 6</h6><p>####### Not a heading 7</p><div><p>Paragraph with <b>bold</b> and <i>italic</i> and <a href="https://example.com">a link</a> and <a href="https://example.com/asd/cat.jpg">an image</a>.</p><p>That also has a right <b>edge bold</b></p><p><code>git commit -m "Yeah"</code> to commit.</p></div><hr><ul><li>An unordered list.</li><li><b>This</b> is a <i>list item</i></li><li>This <a href="https://example.com">cat</a> rocks</li></ul><blockquote>Do or do not.  There is no try.</blockquote><pre><code>def say_hello():\n    print("Hello world!")\n    \nsay_hello()</code></pre><hr><ol><li>An ordered list.</li><li><b>This</b> is a <i>list item</i></li><li>This <a href="https://example.com">cat</a> rocks</li></ol></div>"""
        self.assertEqual(markdown_to_html_node(markdown), expected_result)

        markdown = """1. Gandalf\n2. Bilbo\n3. Sam\n4. Glorfindel\n5. Galadriel\n6. Elrond\n7. Thorin\n8. Sauron\n9. Aragorn"""
        expected_result = """<div><ol><li>Gandalf</li><li>Bilbo</li><li>Sam</li><li>Glorfindel</li><li>Galadriel</li><li>Elrond</li><li>Thorin</li><li>Sauron</li><li>Aragorn</li></ol></div>"""
        self.assertEqual(markdown_to_html_node(markdown), expected_result)

    def test_extract_title(self):
        expected_result = 'Heading 1'

        best_case = '# Heading 1\n\nA paragraph'
        self.assertEqual(extract_title(best_case), expected_result)

        edge_case = '\n# Heading 1\n'
        self.assertEqual(extract_title(edge_case), expected_result)

        edge_case2 = 'A paragraph\n\n# Heading 1\nA paragraph'
        expected_result = 'Heading 1\nA paragraph'
        self.assertEqual(extract_title(edge_case2), expected_result)

        edge_case3 = 'A paragraph\n\n# Heading 1\n\nA paragraph'
        expected_result = 'Heading 1'
        self.assertEqual(extract_title(edge_case3), expected_result)

        fail_case = '\n## Heading 1\n'
        with self.assertRaises(ValueError):
            extract_title(fail_case)

if __name__ == '__main__':
    unittest.main()