import re
from textnode import TextNode
from htmlnode import LeafNode


def text_node_to_html_node(text_node: TextNode):
    if text_node.texttype == "text":
        return LeafNode(tag=None, value=text_node.text)
    if text_node.texttype == "bold":
        return LeafNode(tag="b", value=text_node.text)
    if text_node.texttype == "italic":
        return LeafNode(tag="i", value=text_node.text)
    if text_node.texttype == "code":
        return LeafNode(tag="code", value=text_node.text)
    if text_node.texttype == "link":
        return LeafNode(tag="a", value=text_node.text, props={b"href": text_node.url})
    if text_node.texttype == "image":
        return LeafNode(
            tag="img", value=None, props={"src": text_node.url, "alt": text_node.text}
        )
    else:
        raise Exception("invalid texttype")
