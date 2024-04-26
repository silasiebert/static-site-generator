import unittest
from textnode import TextNode
from leafnode import LeafNode
from utils import (
    split_nodes_delimiter_v2,
    text_node_to_html_node,
    split_nodes_delimiter,
)


class TestUtils(unittest.TestCase):
    def test_text_node_to_html_node(self):
        text_node = TextNode(texttype="text", text="This is normal text")
        html_node = text_node_to_html_node(text_node)
        expected_leaf_node = LeafNode(tag=None, value="This is normal text")
        self.assertEqual(repr(html_node), repr(expected_leaf_node))

    def test_split_nodes_delimiter(self):
        text_type_text = "text"
        text_type_code = "code"

        node = TextNode("This is text with a `code block` word", text_type_text)
        new_nodes = split_nodes_delimiter([node], "`", text_type_code)
        expected_new_nodes = [
            TextNode("This is text with a ", text_type_text),
            TextNode("code block", text_type_code),
            TextNode(" word", text_type_text),
        ]
        self.assertEqual(new_nodes, expected_new_nodes)

    def test_split_nodes_delimiter_v2(self):
        text_type_text = "text"
        text_type_code = "code"

        node = TextNode("This is text with a `code block` word", text_type_text)
        new_nodes = split_nodes_delimiter_v2([node], "`", text_type_code)
        expected_new_nodes = [
            TextNode("This is text with a ", text_type_text),
            TextNode("code block", text_type_code),
            TextNode(" word", text_type_text),
        ]
        self.assertEqual(new_nodes, expected_new_nodes)

    def test_mustiple_bold_words(self):
        text_type_text = "text"
        text_type_bold = "bold"

        node = TextNode(
            "This is text with a *bold* word and a *bold sentence too* aswell.",
            text_type_text,
        )
        new_nodes = split_nodes_delimiter_v2([node], "*", text_type_bold)
        expected_new_nodes = [
            TextNode("This is text with a ", text_type_text),
            TextNode("bold", text_type_bold),
            TextNode(" word and a ", text_type_text),
            TextNode("bold sentence too", text_type_bold),
            TextNode(" aswell.", text_type_text),
        ]
        self.assertEqual(new_nodes, expected_new_nodes)

    def test_delimited_start_and_end(self):
        text_type_text = "text"
        text_type_bold = "bold"

        node = TextNode(
            "*This is a bold sentence* and *bold sentence too*", text_type_text
        )
        new_nodes = split_nodes_delimiter_v2([node], "*", text_type_bold)
        expected_new_nodes = [
            TextNode("This is a bold sentence", text_type_bold),
            TextNode(" and ", text_type_text),
            TextNode("bold sentence too", text_type_bold),
        ]
        self.assertEqual(new_nodes, expected_new_nodes)

    def test_no_delimited_word(self):
        text_type_text = "text"
        text_type_bold = "bold"

        node = TextNode("This is a normal sentence.", text_type_text)
        new_nodes = split_nodes_delimiter_v2([node], "*", text_type_bold)
        expected_new_nodes = [
            TextNode("This is a normal sentence.", text_type_text),
        ]
        self.assertEqual(new_nodes, expected_new_nodes)

    def test_invalid_markdown(self):
        text_type_text = "text"
        text_type_bold = "bold"

        node = TextNode("This is a *normal sentence.", text_type_text)
        with self.assertRaises(ValueError):
            split_nodes_delimiter_v2([node], "*", text_type_bold)
