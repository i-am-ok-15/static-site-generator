import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):

    def test_eq(self):
        node = HTMLNode("p", "this is the paragraph", props={"href": "https://www.google.com"})
        node2 = HTMLNode("p", "this is the paragraph", props={"href": "https://www.google.com"})
        self.assertEqual(node, node2)

    def test_props_to_html(self):
        
        props = {
                "href": "https://www.google.com",
                "target": "_blank",
        }

        node = HTMLNode("p", "this is the paragraph", props=props)
    
    def test_not_eq(self):
        node = HTMLNode("p", "this is the paragraph", props={"href": "https://www.google.com"})
        node2 = HTMLNode("h1", "this is a heading", props={"href": "https://www.google.com"})
        self.assertNotEqual(node, node2)

    def test_repr(self):

        node = HTMLNode("p", "hi", props={"class": "x"})

        self.assertIn("tag='p'", repr(node))
        self.assertIn("value='hi'", repr(node))
        self.assertIn("props={'class': 'x'}", repr(node))