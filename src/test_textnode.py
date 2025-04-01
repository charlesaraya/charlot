import unittest

from textnode import TextNode, TextType

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        bold_node = TextNode("This is a test node", TextType.BOLD)
        same_bold_node = TextNode("This is a test node", TextType.BOLD)
        same_bold_node_and_link = TextNode("This is a test node", TextType.BOLD, "https://charlot.dev")
        diff_bold_node = TextNode("This is a different test node", TextType.BOLD)
        link_node = TextNode("This is a test node", TextType.LINK)

        self.assertEqual(bold_node, same_bold_node)
        self.assertNotEqual(bold_node, diff_bold_node)
        self.assertNotEqual(bold_node, same_bold_node_and_link)
        self.assertNotEqual(bold_node, link_node)
        self.assertEqual(bold_node.url, None)

if __name__ == '__main__':
    unittest.main()