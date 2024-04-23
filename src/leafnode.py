from htmlnode import HTMLNode

class LeafNode(HTMLNode):
    def __init__(self, tag, value=None, props=None):
        if value is None:
            raise ValueError("All leaf nodes require a value")
        super().__init__(tag,value, None, props)

    def to_html(self):
        if self.tag is None:
            return self.value
        else:
            return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
   
