import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_single(self):
        #Test a dictionary with a single property attribute."""
        node = HTMLNode(props={"href": "https://www.google.com"})
        self.assertEqual(node.props_to_html(), ' href="https://www.google.com"')

    def test_props_to_html_multiple(self):
        #Test a dictionary with multiple attributes."""
        node = HTMLNode(
            props={
                "href": "https://www.google.com", 
                "target": "_blank",
            }
        )
        self.assertEqual(node.props_to_html(), ' href="https://www.google.com" target="_blank"')

    def test_props_to_html_empty(self):
        #Test that an empty or missing props dict returns an empty string."""
        node = HTMLNode()
        self.assertEqual(node.props_to_html(), "")

    def test_repr_output(self):
        #Test that the __repr__ method matches the expected format."""
        node = HTMLNode(tag="p", value="Hello World")
        expected_repr = "HTMLNode(tag=p, value=Hello World, children=None, props=None)"
        self.assertEqual(repr(node), expected_repr)

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_p(self):
        #Test a standard paragraph leaf node rendering."""
        node = LeafNode("p", "This is a paragraph of text.")
        self.assertEqual(node.to_html(), "<p>This is a paragraph of text.</p>")

    def test_leaf_to_html_link(self):
        #Test a leaf node link component with properties."""
        node = LeafNode("a", "Click me!", {"href": "https://google.com"})
        self.assertEqual(node.to_html(), '<a href="https://google.com">Click me!</a>')

    def test_leaf_to_html_raw_text(self):
        #Test that a leaf node without a tag renders as raw text."""
        node = LeafNode(None, "Just plain raw text.")
        self.assertEqual(node.to_html(), "Just plain raw text.")

    def test_leaf_to_html_no_value_raises_error(self):
        #Test that a LeafNode missing a value raises a ValueError.
        node = LeafNode("p", None)
        with self.assertRaises(ValueError):
            node.to_html()


    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
        parent_node.to_html(),
        "<div><span><b>grandchild</b></span></div>",
    )

    def test_parent_to_html_with_children(self):
        """Test a parent node with standard leaf node children."""
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        expected = "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>"
        self.assertEqual(node.to_html(), expected)

    def test_parent_to_html_nested_parents(self):
        """Test recursive nesting with parents inside parents."""
        node = ParentNode(
            "div",
            [
                ParentNode(
                    "p",
                    [LeafNode("b", "Nested Bold")],
                ),
                LeafNode(None, "Plain text at root level"),
            ],
        )
        expected = "<div><p><b>Nested Bold</b></p>Plain text at root level</div>"
        self.assertEqual(node.to_html(), expected)

    def test_parent_to_html_no_tag(self):
        """Test that a ParentNode missing a tag raises a ValueError."""
        node = ParentNode(None, [LeafNode("b", "text")])
        with self.assertRaises(ValueError):
            node.to_html()

    def test_parent_to_html_no_children(self):
        """Test that a ParentNode missing children raises a ValueError."""
        node = ParentNode("div", None)
        with self.assertRaises(ValueError):
            node.to_html()


if __name__ == "__main__":
    unittest.main()
