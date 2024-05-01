import unittest
from htmlnode import LeafNode
from textnode import (
    TextNode,
    split_nodes_delimiter_v2,
    split_nodes_link,
    split_nodes_delimiter,
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_image,
)
from utils import markdown_to_blocks, text_node_to_html_node


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
            "This is text with a **bold** word and a **bold sentence too** aswell.",
            text_type_text,
        )
        new_nodes = split_nodes_delimiter_v2([node], "**", text_type_bold)
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

    def test_extract_markdown_images(self):
        text = "This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and ![another](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png)"
        expected_list = [
            (
                "image",
                "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png",
            ),
            (
                "another",
                "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png",
            ),
        ]
        self.assertListEqual(extract_markdown_images(text), expected_list)

    def test_extract_markdown_links(self):
        text = "This is text with a [link](https://www.example.com) and [another](https://www.example.com/another)"
        expected_list = [
            ("link", "https://www.example.com"),
            ("another", "https://www.example.com/another"),
        ]
        self.assertListEqual(extract_markdown_links(text), expected_list)

    def test_extract_markdown_links_missing_bracket(self):
        text = "This is text with a [link(https://www.example.com) and [another](https://www.example.com/another)"
        expected_list = [
            ("link", "https://www.example.com"),
            ("another", "https://www.example.com/another"),
        ]
        self.assertNotEqual(extract_markdown_links(text), expected_list)

    def test_extract_markdown_images_missing_bracket(self):
        text = "This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and !another](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png)"
        expected_list = [
            (
                "image",
                "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png",
            ),
            (
                "another",
                "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png",
            ),
        ]
        self.assertNotEqual(extract_markdown_images(text), expected_list)

    def test_split_nodes_image(self):
        text_type_text = "text"
        text_type_image = "image"
        node = TextNode(
            "This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and another ![second image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png) and some text to end on.",
            text_type_text,
        )
        new_nodes = split_nodes_image([node])
        expected_nodes = [
            TextNode("This is text with an ", text_type_text),
            TextNode(
                "image",
                text_type_image,
                "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png",
            ),
            TextNode(" and another ", text_type_text),
            TextNode(
                "second image",
                text_type_image,
                "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png",
            ),
            TextNode(" and some text to end on.", text_type_text),
        ]
        self.assertListEqual(new_nodes, expected_nodes)

    def test_split_nodes_link(self):
        text_type_text = "text"
        text_type_link = "link"
        node = TextNode(
            "This is text with a [link thingy](https://boot.dev) and another [big search engine](https://www.google.com)",
            text_type_text,
        )
        new_nodes = split_nodes_link([node])
        expected_nodes = [
            TextNode("This is text with a ", text_type_text),
            TextNode(
                "link thingy",
                text_type_link,
                "https://boot.dev",
            ),
            TextNode(" and another ", text_type_text),
            TextNode(
                "big search engine",
                text_type_link,
                "https://www.google.com",
            ),
        ]
        self.assertListEqual(new_nodes, expected_nodes)

    def test_split_nodes_images_invalid_markdown(self):
        node = TextNode(
            "This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and another ![second image]https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png) and some text to end on.",
            "text",
        )
        # TODO: Fix the test
        # with self.assertRaises(ValueError):
        # split_nodes_image([node])

    def test_split_nodes_link_invalid_markdown(self):
        node = TextNode(
            "This is text with an [image(https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and another [second image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png)",
            "text",
        )
        # TODO: Fix the test
        # with self.assertRaises(ValueError):
        #     split_nodes_link([node])

    def test_markdown_to_blocks(self):
        markdown = """
This is **bolded** paragraph

This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

* This is a list
* with items
                   """
        expected_blocks = [
            "This is **bolded** paragraph",
            "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
            "* This is a list\n* with items",
        ]
        blocks = markdown_to_blocks(markdown)
        self.assertListEqual(blocks, expected_blocks)

    def test_markdown_to_blocksLeading_and_trailing_whitespace(self):
        markdown = """



This is **bolded** paragraph

This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line




* This is a list
* with items





                   """
        expected_blocks = [
            "This is **bolded** paragraph",
            "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
            "* This is a list\n* with items",
        ]
        blocks = markdown_to_blocks(markdown)
        self.assertListEqual(blocks, expected_blocks)
