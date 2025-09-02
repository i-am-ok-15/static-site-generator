import re
from textnode import TextNode, TextType
from htmlnode import LeafNode

def text_node_to_html_node(text_node):

    if not isinstance(text_node.text_type, TextType):
        raise ValueError("TextNode has invalid text type")

    if text_node.text_type == TextType.TEXT:
        return LeafNode(tag=None, value=text_node.text)
    if text_node.text_type == TextType.BOLD:
        return LeafNode(tag="b", value=text_node.text)
    if text_node.text_type == TextType.ITALIC:
        return LeafNode(tag="i", value=text_node.text)
    if text_node.text_type == TextType.CODE:
        return LeafNode(tag="code", value=text_node.text)
    if text_node.text_type == TextType.LINK:
        return LeafNode(tag="a", value=text_node.text, props={"href":text_node.url})
    if text_node.text_type == TextType.IMAGE:
        return LeafNode(tag="img", value=text_node.text, props={"src": text_node.url, "alt": text_node.alt})
    raise ValueError(f"Unhandled TextType: {text_node.text_type}")

def split_nodes_delimiter(old_nodes, delimiter, text_type):

    new_nodes = []

    for node in old_nodes:

        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        
        parts = node.text.split(delimiter)

        if len(parts) % 2 == 0:
            raise Exception(f"Unpaired {delimiter} in {node.text}")

        for i, part in enumerate(parts):
            if i % 2 == 0:
                if part == "":
                    continue
                even_node = TextNode(part, TextType.TEXT)
                new_nodes.append(even_node)
            else:
                odd_node = TextNode(part, text_type)
                new_nodes.append(odd_node)
 
    return new_nodes

def extract_markdown_images(text):

    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def extract_markdown_links(text):

    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def split_nodes_image(old_nodes):

    new_nodes = []

    for node in old_nodes:

        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        text = node.text

        images = extract_markdown_images(text)

        if not images:
            new_nodes.append(node)
            continue

        for alt, link in images:
            before, text = text.split(f"![{alt}]({link})", 1)
            if before:
                new_nodes.append(TextNode(before, TextType.TEXT))
            new_nodes.append(TextNode(alt, TextType.IMAGE, link))
        if text:
            new_nodes.append(TextNode(text, TextType.TEXT))
        
    return new_nodes

def split_nodes_link(old_nodes):

    new_nodes = []

    for node in old_nodes:

        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        text = node.text

        links = extract_markdown_links(text)

        if not links:
            new_nodes.append(node)
            continue

        for alt, link in links:
            before, text = text.split(f"[{alt}]({link})", 1)
            if before:
                new_nodes.append(TextNode(before, TextType.TEXT))
            new_nodes.append(TextNode(alt, TextType.LINK, link))
        if text:
            new_nodes.append(TextNode(text, TextType.TEXT))
        
    return new_nodes