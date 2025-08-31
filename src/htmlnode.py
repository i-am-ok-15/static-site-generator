
class HTMLNode:

    def __init__(self, tag=None, value=None, children=None, props=None):

        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):

        raise NotImplementedError
    
    def props_to_html(self):
        
        print(self)
        html_string = ""
        for key, value in self.props.items():
            html_string += f" {key}=\"{value}\""

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
