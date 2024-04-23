import unittest
from leafnode import LeafNode

class TestLeafnode(unittest.TestCase):
    def test_value(self):
        pass
    
    def test_paragraph(self):
        leaf = LeafNode("p", "This is a paragraph of text.")
        expected_html = "<p>This is a paragraph of text.</p>"
        self.assertEqual(leaf.to_html(), expected_html)

    def test_link(self):
        leaf = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        expected_html ="<a href=\"https://www.google.com\">Click me!</a>"
        self.assertEqual(leaf.to_html(), expected_html)
    
    def test_no_tag(self):
        leaf = LeafNode(None, "Raw text", {"href": "https://www.google.com"})
        expected_html = "Raw text"
        self.assertEqual(leaf.to_html(), expected_html)

    def test_no_value(self):
        with self.assertRaises(ValueError):
            LeafNode("p")

if __name__ == "__main__":
    unittest.main()
