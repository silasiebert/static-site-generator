from htmlnode import HTMLNode

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag == None:
            raise ValueError("tag parameter required")
        if self.children == None or len(self.children) == 0:
            raise ValueError("there are no child nodes")
        html = f"<{self.tag}>"

        for node in self.children:
            html += node.to_html()

        html += f"</{self.tag}>"

        return html
