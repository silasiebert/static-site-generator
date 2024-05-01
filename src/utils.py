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


def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    print(blocks)
    clean_blocks = map(lambda string: string.strip(" \n"), blocks)
    print(clean_blocks)
    non_empty_blocks = filter(lambda block: block != "", clean_blocks)
    block_list = list(non_empty_blocks)
    print(block_list)
    return block_list
