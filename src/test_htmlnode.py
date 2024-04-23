import unittest

from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_props(self):
        node = HTMLNode(props={"href": "https://boot.dev", "target": "_blank"})
        expected_html = " href=\"https://boot.dev\" target=\"_blank\""

        self.assertEqual(node.props_to_html(), expected_html)

    def test_repr(self):
        children = []
        children.append(HTMLNode("text"))
        node = HTMLNode("text", "This is some text", children,{"href": "https://boot.dev", "target": "_blank"})
        expected_html = "HTMLNode(tag=text value=This is some text children=[HTMLNode(tag=text value=None children=None props=)] props= href=\"https://boot.dev\" target=\"_blank\")"
        print(node.__repr__)
        self.assertEqual(repr(node), expected_html)

if __name__ == "__main__":
    unittest.main(verbosity=2)
