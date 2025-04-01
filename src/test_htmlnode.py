import unittest

from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_html(self):
        link_props = {
            "href": "https://www.example.com",
            "target": "_blank",
            "rel": "noopener noreferrer",
            "title": "Visit Example"
        }
        link_node = HTMLNode(tag="a", value="Click bait!", props=link_props) 
        h1_node = HTMLNode(tag="h1", value="An important title")
        p_node = HTMLNode(tag="p", value="Lorem ipsum dolor sit amet", children=[link_node])
        body_node = HTMLNode(tag="body", children=[h1_node, p_node])

        self.assertEqual(link_node.props_to_html(), ' href="https://www.example.com" target="_blank" rel="noopener noreferrer" title="Visit Example"')
        self.assertEqual(h1_node.props_to_html(), '')
        self.assertIn(p_node, body_node.children)

class TestLeafNode(unittest.TestCase):
    def test_leaf(self):
        link_props = {
            "href": "https://www.example.com",
            "target": "_blank"
        }
        p_node = LeafNode("p", "This is a paragraph of text.")
        raw_node = LeafNode(None, "This is a paragraph of text.")
        no_child_node = LeafNode(None, "This is a paragraph of text.", [p_node])
        link_node = LeafNode(tag="a", value="Click bait!", props=link_props) 

        self.assertEqual(p_node.to_html(), '<p>This is a paragraph of text.</p>')
        self.assertEqual(raw_node.to_html(), 'This is a paragraph of text.')
        self.assertEqual(no_child_node.children, None)
        self.assertEqual(link_node.props_to_html(), ' href="https://www.example.com" target="_blank"')

if __name__ == '__main__':
    unittest.main()