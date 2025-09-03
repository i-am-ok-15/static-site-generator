import unittest

from textnode import TextNode, TextType
from converters import text_node_to_html_node, split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link, text_to_textnodes

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

    def test_split_delimiter_bold(self):

        markdown_string = "this is a test message for my **bold markdown 1**"
        delimiter = "**"
        text_type = "BOLD"

        node = TextNode(markdown_string, TextType.TEXT)

        split_nodes_delimiter([node], delimiter, text_type)
    
    def test_split_delimiter_italic(self):

        markdown_string = "this is a test message for my _italic markdown 1_"
        delimiter = "_"
        text_type = "ITALIC"

        node = TextNode(markdown_string, TextType.TEXT)

        split_nodes_delimiter([node], delimiter, text_type)
    
    def test_split_delimiter_code(self):

        markdown_string = "this is a test message for my `bold markdown 1`"
        delimiter = "`"
        text_type = "CODE"

        node = TextNode(markdown_string, TextType.TEXT)

        split_nodes_delimiter([node], delimiter, text_type)

    def test_extract_markdown_images(self):

        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):

        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev)"
        )
        self.assertListEqual([("to boot dev", "https://www.boot.dev")], matches)

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])

        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_links(self):

        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
    TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])

        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode(
                    "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
                ),
            ],
            new_nodes,
        )
    
    def test_text_to_textnodes(self):

        text = """This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"""
        
        new_nodes = text_to_textnodes(text)

        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            new_nodes,
        )