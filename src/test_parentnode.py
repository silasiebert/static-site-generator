import unittest
from parentnode import ParentNode
from leafnode import LeafNode

class TestParentNode(unittest.TestCase):
    def test_to_html(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        expected_html = "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>" 
        self.assertEqual(node.to_html(), expected_html) 

    def test_nested(self):
        nested_node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )

        
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                nested_node,
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )

        
        expected_html = "<p><b>Bold text</b><p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p><i>italic text</i>Normal text</p>" 
        self.assertEqual(node.to_html(), expected_html) 

    def test_no_tag(self):
        with self.assertRaises(ValueError):
            node = ParentNode(
                None,
                [
                    LeafNode("b", "Bold text"),
                    LeafNode("i", "italic text"),
                    LeafNode(None, "Normal text"),
                ],
            )
            node.to_html()


    def test_no_children(self):
        with self.assertRaises(ValueError):
            node = ParentNode("p", None)
            node.to_html()


if __name__ == '__main__':
    unittest.main()
