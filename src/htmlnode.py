from textnode import TextNode, text_to_textnodes
from markdown_blocks import MarkdownBlock, block_to_block_type, markdown_to_blocks
import re


class HTMLNode:
    def __init__(self, tag=None, value=None, children: list = None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError()

    def props_to_html(self):
        result = ""
        if self.props is not None:
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
    def __init__(self, tag, children: list[HTMLNode], props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        print(f"Children type: {type(self.children)}")
        if self.tag is None:
            raise ValueError("tag parameter required")
        if self.children is None or len(self.children) == 0:
            raise ValueError("there are no child nodes")
        html = f"<{self.tag}>"

        for node in self.children:
            html += node.to_html()

        html += f"</{self.tag}>"

        return html


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


def quote_block_to_html(block):
    clean_quote = "\n".join(map(lambda line: line.lstrip("> "), block.split("\n")))
    html_quote_node = LeafNode("blockquote", clean_quote)
    return html_quote_node


def unordered_block_to_html(block):
    clean_list = "\n".join(map(lambda line: line.lstrip("*- "), block.split("\n")))
    node_map = map(lambda item: LeafNode("li", item), clean_list.split("\n"))
    node_list = list(node_map)
    list_node = ParentNode("ul", node_list)
    return list_node


def ordered_block_to_html(block):
    clean_list = "\n".join(map(lambda line: line[3::], block.split("\n")))
    node_map = map(lambda item: LeafNode("li", item), clean_list.split("\n"))
    node_list = list(node_map)
    list_node = ParentNode("ol", node_list)
    return list_node


def code_block_to_html_node(block):
    clean_code = block.strip("```")
    code_node = LeafNode("code", clean_code)
    pre_node = ParentNode("pre", [code_node])
    return pre_node


def heading_block_to_html_node(block):
    heading_prefix = re.search(r"(^#{1,6})", block).group(1)
    clean_heading = block.lstrip(heading_prefix + " ")
    heading_size = len(heading_prefix)
    heading_node = LeafNode(f"h{heading_size}", clean_heading)
    return heading_node


def paragraph_block_to_html_node(block):
    text_nodes = text_to_textnodes(block)
    html_nodes = map(text_node_to_html_node, text_nodes)
    pararagraph_parent_node = ParentNode("p", list(html_nodes))
    return pararagraph_parent_node


def markdown_to_html_node(markdown):
    root_child_nodes = []
    block_list = markdown_to_blocks(markdown)
    print(f"Block list is {block_list}")
    for block in block_list:
        block_type = block_to_block_type(block)
        print(f"Block type is {block_type}")
        match block_type:
            case MarkdownBlock.block_type_quote:
                root_child_nodes.append(quote_block_to_html(block))
            case MarkdownBlock.block_type_unordered_list:
                root_child_nodes.append(unordered_block_to_html(block))
            case MarkdownBlock.block_type_ordered_list:
                root_child_nodes.append(ordered_block_to_html(block))
            case MarkdownBlock.block_type_code:
                root_child_nodes.append(code_block_to_html_node(block))
            case MarkdownBlock.block_type_heading:
                root_child_nodes.append(heading_block_to_html_node(block))
            case MarkdownBlock.block_type_paragraph:
                root_child_nodes.append(paragraph_block_to_html_node(block))
    root_node = ParentNode("div", root_child_nodes)
    return root_node
