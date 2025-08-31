import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


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
    
    def test_leaf_to_html_p(self):

        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
    

    def test_leaf_to_html_b(self):

        node = LeafNode("b", "Hello, world!")
        self.assertEqual(node.to_html(), "<b>Hello, world!</b>")

    def test_leaf_to_html_link(self):
        node = LeafNode("a", "Google", props={"href": "https://www.google.com",})
        print("**************************")
        print(node.to_html())
        print("**************************")
        self.assertEqual(node.to_html(), """<a href="https://www.google.com">Google</a>""")
    
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )