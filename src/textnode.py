class TextNode:
    def __init__(self, text, texttype, url=None):
        self.text = text
        self.texttype = texttype
        self.url = url

    def __eq__(self, other):
        return self.text == other.text and self.texttype == other.texttype and self.url == other.url
    
    def __repr__(self) -> str:
        return f"TextNode({self.text}, {self.texttype}, {self.url})"
