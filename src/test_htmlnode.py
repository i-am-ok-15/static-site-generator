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
    
    def test_to_html_with_tree(self):
        fourth_tier_a = LeafNode("b", "leafnode")
        fourth_tier_b = LeafNode("b", "leafnode")

        third_tier_one = LeafNode("span", "leafnode")
        third_tier_two = LeafNode("span", "leafnode")
        third_tier_three = ParentNode("span", [fourth_tier_a, fourth_tier_b])

        second_tier_a = ParentNode("p", [third_tier_one, third_tier_two])
        second_tier_b = ParentNode("p", [third_tier_three])

        first_tier_one = ParentNode("div", [second_tier_a, second_tier_b])

        self.assertEqual(
            first_tier_one.to_html(),
            "<div><p><span>leafnode</span><span>leafnode</span></p><p><span><b>leafnode</b><b>leafnode</b></span></p></div>",
        )

        