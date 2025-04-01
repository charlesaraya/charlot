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

if __name__ == '__main__':
    unittest.main()