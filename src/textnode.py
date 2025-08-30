from enum import Enum

class TextType(Enum):
    plain_text = ""
    bold_text = "**"
    italic_text = "_"
    code_text = "`"
    link_text = f"[{anchor_text}]({url_text})"
    image_text = f"![{alt_text}]({url_text})"
