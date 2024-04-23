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
            for prop,value in self.props.items():
                result += f" {prop}=\"{value}\""
        return result


    def __repr__(self): 
        return f"HTMLNode(tag={self.tag} value={self.value} children={self.children} props={self.props_to_html()})"
