import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):

    def test_eq(self):
        node = HTMLNode("p", "this is the paragraph", props={"href": "https://www.google.com"})
        node2 = HTMLNode("p", "this is the paragraph", props={"href": "https://www.google.com"})
        self.assertEqual(node, node2)