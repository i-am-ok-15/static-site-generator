
class HTMLNode:

    def __init__(self, tag=None, value=None, children=None, props=None):

        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):

        raise NotImplementedError
    
    def props_to_html(self):
        
        if not self.props:
            return ""
        html_string = ""
        for key, value in self.props.items():
            html_string += f" {key}=\"{value}\""
        return html_string

    def __eq__(self, other):

        if not isinstance(self, HTMLNode):
            return NotImplemented
        return (
            self.tag == other.tag and
            self.value == other.value and
            self.children == other.children and
            self.props == other.props
        )

    def __repr__(self):

        return f"HTMLNode(tag={self.tag!r}, value={self.value!r}, children={self.children!r}, props={self.props!r})"


class LeafNode(HTMLNode):

    def __init__(self, tag, value, props=None):
        
        if not value:
            raise ValueError("LeafNode must have a value")
        super().__init__(tag=tag, value=value, children=None, props=props)
  
    def to_html(self):

        if not self.value:
            raise ValueError("LeafNode must have a value")   

        if not self.tag:
            return f"{self.value}"
        
        attributes = self.props_to_html()
        return f"<{self.tag}{attributes}>{self.value}</{self.tag}>"