from functools import reduce


class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError()

    def props_to_html(self):
        result = ""
        if self.props != None:
            for prop, value in self.props.items():
                result += f' {prop}="{value}"'
        return result

    def __repr__(self):
        return f"HTMLNode(tag={self.tag} value={self.value} children={self.children} props={self.props_to_html()})"


class LeafNode(HTMLNode):
    def __init__(self, tag, value=None, props=None):
        if value is None:
            raise ValueError("All leaf nodes require a value")
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.tag is None:
            return self.value
        else:
            return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"


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
