import pytest

from htmlnode import HTMLNode, markdown_to_html_node, ParentNode


class TestHTMLNode:
    def test_props(self):
        node = HTMLNode(props={"href": "https://boot.dev", "target": "_blank"})
        expected_html = ' href="https://boot.dev" target="_blank"'

        assert node.props_to_html() == expected_html

    def test_repr(self):
        children = []
        children.append(HTMLNode("text"))
        node = HTMLNode(
            "text",
            "This is some text",
            children,
            {"href": "https://boot.dev", "target": "_blank"},
        )
        expected_html = 'HTMLNode(tag=text value=This is some text children=[HTMLNode(tag=text value=None children=None props=)] props= href="https://boot.dev" target="_blank")'
        print(node.__repr__)
        assert repr(node) == expected_html


@pytest.mark.parametrize(
    "markdown, expected_html",
    [
        (
            """- This is the first line
* this is the second line""",
            """<div><ul><li>This is the first line</li><li>this is the second line</li></ul></div>""",
        ),
        (
            """# Heading 1

Paragraph text here.""",
            """<div><h1>Heading 1</h1><p>Paragraph text here.</p></div>""",
        ),
        (
            """1. First item
2. Second item""",
            """<div><ol><li>First item</li><li>Second item</li></ol></div>""",
        ),
        (
            """> Blockquote text""",
            """<div><blockquote>Blockquote text</blockquote></div>""",
        ),
        (
            """```
Code block here
```""",
            """<div><pre><code>
Code block here
</code></pre></div>""",
        ),
    ],
)
def test_markdown_to_htmlnode(markdown, expected_html):
    html_node: ParentNode
    html_node = markdown_to_html_node(markdown)
    assert html_node.to_html() == expected_html
