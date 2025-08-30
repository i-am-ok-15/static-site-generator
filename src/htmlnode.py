

class HTMLNode:

    def __init__(self, tag=None, value=None, children=None, props=None):

        self.tag = tag
        self.value = value
        self.children = children
        self.props = props


    def to_html(self):

        raise NotImplementedError
    

    def props_to_html(self):
        
        html_string = ""
        for key, value in self.items():
            html_string + f" {key}=\"{value}\""
    
    def __repr__(self):

        print("===================")
        print(self)
        print("===================")
        print(
            self.tag,
            self.value,
            self.children,
            self.props
        )        
        print("===================")
