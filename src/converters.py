import re
from textnode import TextNode, TextType
from blocknode import BlockType
from htmlnode import HTMLNode, ParentNode, LeafNode

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

def text_to_textnodes(text):

    text_node = [TextNode(text, TextType.TEXT)]

    new_nodes = split_nodes_image(text_node)
    new_nodes = split_nodes_link(new_nodes)
    new_nodes = split_nodes_delimiter(new_nodes, "`", TextType.CODE)
    new_nodes = split_nodes_delimiter(new_nodes, "**", TextType.BOLD)
    new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)

    return new_nodes

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

def markdown_to_blocks(markdown):

    blocks = markdown.split("\n\n")

    stripped_blocks = []

    for block in blocks:
        stripped_block = block.strip()
        stripped_blocks.append(stripped_block)
    
    clean_blocks = []

    for block in stripped_blocks:
        if len(block) == 0:
            pass
        else:
            clean_blocks.append(block)

    return clean_blocks

def block_to_block_type(markdown):

    if markdown.startswith("#"):
        hash_count = 0
        while hash_count < len(markdown) and markdown[hash_count] == "#" and hash_count < 6:
            hash_count += 1
        if 1 <= hash_count <= 6 and hash_count < len(markdown) and markdown[hash_count] == " " and hash_count + 1 < len(markdown):
            return BlockType.HEADING

    list_check = markdown.split("\n")

    if list_check[0] == "```":
        if len(list_check) >= 2 and list_check[0] == "```" and list_check[-1] == "```":
            return BlockType.CODE
    
    if list_check[0].startswith(">"):
        is_quote = True
        for line in list_check:
            if not line.startswith(">"):
                is_quote = False
                break
        if is_quote:
            return BlockType.QUOTE

    if list_check[0].startswith("- "):
        is_unordered_list = True
        for i in range(len(list_check)):
            if not list_check[i].startswith("- "):
                is_unordered_list = False
                break
        if is_unordered_list:
            return BlockType.UNORDERED_LIST
    
    if list_check[0].startswith("1. "):
        is_ordered_list = True
        for i in range(len(list_check)):
            number = i + 1
            if not list_check[i].startswith(f"{number}. "):
                is_ordered_list = False
                break
        if is_ordered_list:
            return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH

def markdown_to_html_node(markdown):
    
    html_children = []

    blocks = markdown_to_blocks(markdown)

    for block in blocks:
        block_type = block_to_block_type(block)

        if block_type == BlockType.HEADING:
            node = heading_to_htmlnode(block) # complete

        elif block_type == BlockType.CODE:
            node = code_to_htmlnode(block)

        elif block_type == BlockType.QUOTE:
            node = quote_to_htmlnode(block) # complete

        elif block_type == BlockType.UNORDERED_LIST:
            node = unordered_list_to_htmlnode(block)

        elif block_type == BlockType.ORDERED_LIST:
            node = ordered_list_to_htmlnode(block)

        else:
            node = paragraph_to_htmlnode(block) # complete
        
        if node is not None:
            html_children.append(node)        


    return HTMLNode(tag="div", children=html_children)

def heading_to_htmlnode(block):

    heading_level = 0

    for char in block:
        if char == "#":
            heading_level += 1
        else:
            break
    
    if not 1 <= heading_level <= 6:
        return None
    
    if block[heading_level:heading_level + 1] != " ":
        return None
    
    heading_text = block[heading_level + 1:].strip()
    heading_tag = f"h{heading_level}"
    children = text_to_children(heading_text)
    
    return HTMLNode(tag=heading_tag, children=children)
    
def code_to_htmlnode(block):
    pass

def quote_to_htmlnode(block):

    lines = block.split("\n")

    quote_text = []

    is_quote = True
    for line in lines:
        if not line.startswith("> "):
            is_quote = False
            break
        if line == "> ":
            quote_text.append("")
        else:
            line = line.rstrip()
            quote_text.append(line[2:])

    if is_quote:
        quote_text = "\n".join(quote_text)
        children = text_to_children(quote_text)

        return HTMLNode("blockquote", children=children)

    else:
        return paragraph_to_htmlnode(block)

def unordered_list_to_htmlnode(block):
    
    lines = block.split("\n")

    items_text = []

    for line in lines:
        if not line.startswith("- "):
            continue
        line = line.rstrip()
        items_text.append(line[2:])
    
    if items_text:
        list_nodes = []
        for item in items_text:
            s = item.strip()
            if s:
                list_text = text_to_children(item)
                if list_text:
                    list_html = ParentNode("li", children=list_text)
                    list_nodes.append(list_html)

        if list_nodes:
            wrapped_list_html = ParentNode("ul", children=list_nodes)

            return wrapped_list_html

        return None
    
    else:
        return None

def ordered_list_to_htmlnode(block):
    pass

def paragraph_to_htmlnode(block):
    
    lines = block.split("\n")
    clean_lines = []

    for line in lines:
        line = line.strip()
        if not line:
            continue
        clean_lines.append(line)

    clean_text = " ".join(clean_lines)
    if not clean_text:
        return None
    
    children =  text_to_children(clean_text)
    if not children:
        return None

    return HTMLNode("p", children=children)

def text_to_children(clean_text):
    
    text_nodes = text_to_textnodes(clean_text)
    html_nodes = []

    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        html_nodes.append(html_node)

    return html_nodes
