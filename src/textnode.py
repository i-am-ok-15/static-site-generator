from enum import Enum

class TextType(Enum):
    plain_text = ""
    bold_text = "**"
    italic_text = "_"
    code_text = "`"
    link_text = f"[anchor text](url)"
    image_text = f"![alt_text](url)"

class TextNode:
    
    def __init__(self, text, text_type, url=None):

        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, text_node):

        if self.text == text_node.text:
            if self.text_type == text_node.text_type:
                if self.url == text_node.url:
                    return True
        return False
    
    def __repr__(self):

        return f"TextNode ({self.text}, {self.text_type}, {self.url})"