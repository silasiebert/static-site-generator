import re
from textnode import TextNode
from htmlnode import LeafNode

text_type_text = "text"
text_type_bold = "bold"
text_type_italic = "italic"
text_type_code = "code"
text_type_link = "link"
text_type_image = "image"


def text_node_to_html_node(text_node: TextNode):
    if text_node.texttype == text_type_text:
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


def split_nodes_delimiter(old_nodes: list[TextNode], delimiter, text_type):
    new_nodes = []
    old_node: TextNode
    for old_node in old_nodes:
        print(f"Old node: {old_node}")
        if old_node.texttype != text_type_text or delimiter not in old_node.text:
            new_nodes.append(old_node)
        else:
            word: str
            current_word_list = []
            current_text_type = text_type_text
            has_closing_delimiter = True
            for word in old_node.text.split():
                if word.startswith(delimiter):
                    if len(current_word_list) != 0:
                        current_segment = " ".join(current_word_list) + " "
                        if len(current_word_list) == 1:
                            current_segment = " " + " ".join(current_word_list) + " "
                        new_textnode = TextNode(
                            text=current_segment, texttype=current_text_type
                        )
                        new_nodes.append(new_textnode)
                        current_word_list = []
                    word = word.removeprefix(delimiter)
                    current_text_type = text_type
                    has_closing_delimiter = False
                if word.endswith(delimiter):
                    current_word_list.append(word.removesuffix(delimiter))
                    new_textnode = TextNode(
                        text=" ".join(current_word_list), texttype=current_text_type
                    )
                    new_nodes.append(new_textnode)
                    has_closing_delimiter = True
                    current_text_type = text_type_text
                    current_word_list = []

                if delimiter not in word:
                    current_word_list.append(word)
            if len(current_word_list) != 0:
                new_textnode = TextNode(
                    text=" " + " ".join(current_word_list), texttype=current_text_type
                )
                new_nodes.append(new_textnode)
                current_word_list = []

            print(f"New nodes: {new_nodes}")

            if not has_closing_delimiter:
                raise Exception(f"missing closing {delimiter}")
    return new_nodes


def split_nodes_delimiter_v2(old_nodes: list[TextNode], delimiter, text_type):
    old_node: TextNode
    new_nodes = []
    for old_node in old_nodes:
        text_segments_list = old_node.text.split(delimiter)
        if len(text_segments_list) % 2 == 0:
            raise ValueError(
                f"Invalid markdown syntax: Missing {delimiter} closing tag."
            )
        for i in range(0, len(text_segments_list)):
            if text_segments_list[i] != "":
                if i % 2 == 0:
                    new_node = TextNode(
                        text=text_segments_list[i], texttype=text_type_text
                    )
                else:
                    new_node = TextNode(text=text_segments_list[i], texttype=text_type)
                new_nodes.append(new_node)
    return new_nodes


def extract_markdown_images(text):
    regex = r"!\[(.*?)\]\((.*?)\)"
    return re.findall(regex, text)


def extract_markdown_links(text):
    regex = r"\[(.*?)\]\((.*?)\)"
    return re.findall(regex, text)


def split_nodes_image(old_nodes: list[TextNode]):
    old_node: TextNode
    new_nodes: list[TextNode]
    new_nodes = []
    for old_node in old_nodes:
        if old_node.texttype != text_type_text:
            new_nodes.append(old_node)
            continue
        text: str
        image_tups = extract_markdown_images(old_node.text)
        if len(image_tups) > 0:
            text = old_node.text
            for image_tup in image_tups:
                text_segments = text.split(f"![{image_tup[0]}]({image_tup[1]})", 1)
                if len(text_segments) != 2:
                    raise ValueError("Invalid mardown syntax, image section not closed")
                if text_segments[0] != "":
                    new_nodes.append(
                        TextNode(text=text_segments[0], texttype=text_type_text)
                    )
                new_nodes.append(
                    TextNode(
                        text=image_tup[0], texttype=text_type_image, url=image_tup[1]
                    )
                )
                text = text_segments[1]
            if text != "":
                new_nodes.append(TextNode(text=text, texttype=text_type_text))
        else:
            new_nodes.append(old_node)
    return new_nodes


def split_nodes_link(old_nodes: list[TextNode]):
    old_node: TextNode
    new_nodes: list[TextNode]
    new_nodes = []
    for old_node in old_nodes:
        if old_node.texttype != text_type_text:
            new_nodes.append(old_node)
            continue
        text: str
        text = old_node.text
        link_tups = extract_markdown_links(text)
        if len(link_tups) > 0:
            for link_tup in link_tups:
                text_segments = text.split(f"[{link_tup[0]}]({link_tup[1]})", 1)
                if len(text_segments) != 2:
                    raise ValueError("Invalid markdown syntax, link section not closed")
                if text_segments[0] != "":
                    new_nodes.append(
                        TextNode(text=text_segments[0], texttype=text_type_text)
                    )
                new_nodes.append(
                    TextNode(text=link_tup[0], texttype=text_type_link, url=link_tup[1])
                )
                text = text_segments[1]
            if text != "":
                new_nodes.append(
                    TextNode(text=text_segments[1], texttype=text_type_text)
                )
        else:
            new_nodes.append(old_node)
    return new_nodes
