import unittest

from textnode import TextNode, TextType
from converters import text_node_to_html_node

class TestConverters(unittest.TestCase):

    def test_text(self):
        text_node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
    
    def test_text_to_html_bold(self):

        bold_node = TextNode("This is a bold node", TextType.BOLD)
        html_node = text_node_to_html_node(bold_node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.to_html(), "<b>This is a bold node</b>")

    def test_text_to_html_italic(self):

        italic_node = TextNode("This is an italic node", TextType.ITALIC)
        html_node = text_node_to_html_node(italic_node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.to_html(), "<i>This is an italic node</i>")

    def test_text_to_html_code(self):

        code_node = TextNode("This is a code node", TextType.CODE)
        html_node = text_node_to_html_node(code_node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.to_html(), "<code>This is a code node</code>")

    def test_text_to_html_link(self):

        link_node = TextNode("This is a link node", TextType.LINK, url="www.linktest.com")
        html_node = text_node_to_html_node(link_node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.to_html(), """<a href="www.linktest.com">This is a link node</a>""")

    def test_text_to_html_image(self):

        image_node = TextNode("This is an image node", TextType.IMAGE, url="www.imagelink.com", alt="this is a test image")
        html_node = text_node_to_html_node(image_node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.to_html(), """<img src="www.imagelink.com" alt="this is a test image">This is an image node</img>""")
