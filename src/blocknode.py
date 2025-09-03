from enum import Enum

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered list"
    ORDERED_LIST = "ordered list"

# class TextNode:
    
#     def __init__(self, text, text_type, url=None, alt=None):

#         self.text = text
#         self.text_type = text_type
#         self.url = url
#         self.alt = alt

#     def __eq__(self, other):

#         if not isinstance(self, TextNode):
#             return NotImplemented
#         return (
#             self.text == other.text and
#             self.text_type == other.text_type and
#             self.url == other.url
#         )
    
#     def __repr__(self):
#         text_type_val = getattr(self.text_type, "value", self.text_type)
#         return f"TextNode({self.text}, {text_type_val}, {self.url})"