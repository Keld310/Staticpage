import unittest
from textnode import TextNode, TextType, text_node_to_html_node
from inline_markdown import split_nodes_image, split_nodes_link


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_eq_with_url(self):
        #Test that two identical nodes with matching URLs are equal.
        node = TextNode("Click here", TextType.LINK, "https://boot.dev")
        node2 = TextNode("Click here", TextType.LINK, "https://boot.dev")
        self.assertEqual(node, node2)

    def test_not_eq_different_types(self):
        #Test that nodes with different text types are not equal.
        node = TextNode("Hello World", TextType.TEXT)
        node2 = TextNode("Hello World", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_not_eq_missing_url(self):
        #Test that one node with a URL and one without are not equal.
        node = TextNode("Click here", TextType.LINK, "https://boot.dev")
        node2 = TextNode("Click here", TextType.LINK, None)
        self.assertNotEqual(node, node2)

    def test_not_eq_different_text(self):
        #Test that nodes with different text content are not equal.
        node = TextNode("Apple", TextType.BOLD)
        node2 = TextNode("Banana", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_text_node_to_html_node_normal(self):
        """Test conversion of a plain text node."""
        node = TextNode("Plain text", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertIsNone(html_node.tag)
        self.assertEqual(html_node.value, "Plain text")

    def test_text_node_to_html_node_bold(self):
        """Test conversion of a bold text node."""
        node = TextNode("Bold text", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "Bold text")

    def test_text_node_to_html_node_image(self):
        """Test conversion of an image text node with alt text and a source URL."""
        node = TextNode("Alt text description", TextType.IMAGE, "https://boot.dev")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {"src": "https://boot.dev", "alt": "Alt text description"})

    def test_text_node_to_html_node_invalid(self):
        """Test that an unsupported text type causes a ValueError exception."""
        # Creating a mockup or passing an unhandled variation to trigger the exception block
        class FakeType:
            value = "fake"
        node = TextNode("Errors", FakeType)
        with self.assertRaises(ValueError):
            text_node_to_html_node(node)

    def test_eq_identical_nodes(self):
        """Verify that two identical TextNodes evaluate as equal."""
        node1 = TextNode("Hello world", TextType.TEXT)
        node2 = TextNode("Hello world", TextType.TEXT)
        self.assertEqual(node1, node2)

    def test_not_eq_different_types(self):
        """Verify nodes with different TextTypes do not evaluate as equal."""
        node1 = TextNode("Hello world", TextType.TEXT)
        node2 = TextNode("Hello world", TextType.BOLD)
        self.assertNotEqual(node1, node2)

    def test_not_eq_different_urls(self):
        """Verify nodes with mismatching URLs do not evaluate as equal."""
        node1 = TextNode("Link Text", TextType.LINK, "https://boot.dev")
        node2 = TextNode("Link Text", TextType.LINK, "https://google.com")
        self.assertNotEqual(node1, node2)


    # --- 2. HTML Conversion Tests ---

    def test_text_to_html_normal(self):
        """Verify conversion of a NORMAL node into a plain LeafNode."""
        node = TextNode("Plain text string", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertIsNone(html_node.tag)
        self.assertEqual(html_node.value, "Plain text string")

    def test_text_to_html_image(self):
        """Verify image properties translate correctly into HTML props."""
        node = TextNode("Alt caption", TextType.IMAGE, "https://example.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertDictEqual(html_node.props, {"src": "https://example.com", "alt": "Alt caption"})


    # --- 3. Image Node Splitting Tests ---

    def test_split_image_basic(self):
        """Test splitting text with a single image block."""
        node = TextNode("Hello ![logo](https://boot.dev) world", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        
        expected = [
            TextNode("Hello ", TextType.TEXT),
            TextNode("logo", TextType.IMAGE, "https://boot.dev"),
            TextNode(" world", TextType.TEXT)
        ]
        self.assertListEqual(new_nodes, expected)

    def test_split_image_multiple(self):
        """Test splitting sequentially across multiple image matches."""
        node = TextNode("![one](url1.jpg) middle ![two](url2.png)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        
        expected = [
            TextNode("one", TextType.IMAGE, "url1.jpg"),
            TextNode(" middle ", TextType.TEXT),
            TextNode("two", TextType.IMAGE, "url2.png")
        ]
        self.assertListEqual(new_nodes, expected)

    def test_split_image_ignores_non_normal_nodes(self):
        """Ensure already formatted nodes (like BOLD) bypass splitting entirely."""
        node = TextNode("Ignore this ![pic](url.png)", TextType.BOLD)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(new_nodes, [node])


    # --- 4. Link Node Splitting Tests ---

    def test_split_link_basic(self):
        """Test splitting text with a single standard Markdown link."""
        node = TextNode("Go to [Boot.dev](https://boot.dev) for lessons", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        
        expected = [
            TextNode("Go to ", TextType.TEXT),
            TextNode("Boot.dev", TextType.LINK, "https://boot.dev"),
            TextNode(" for lessons", TextType.TEXT)
        ]
        self.assertListEqual(new_nodes, expected)

    def test_split_link_empty_anchor(self):
        """Verify handling of links with an empty text anchor string."""
        node = TextNode("Empty [](https://blank.com) link", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        
        expected = [
            TextNode("Empty ", TextType.TEXT),
            TextNode("", TextType.LINK, "https://blank.com"),
            TextNode(" link", TextType.TEXT)
        ]
        self.assertListEqual(new_nodes, expected)


    # --- 5. Pipeline Chain Integration Test ---

    def test_chaining_splitters(self):
        """Ensure image and link splitters can be chained sequentially over raw blocks."""
        raw_node = TextNode(
            "Welcome to [GitHub](https://github.com) check out this ![icon](icon.png) file", 
            TextType.TEXT
        )
        
        # Pass through the image splitter first, then pass that output to the link splitter
        after_images = split_nodes_image([raw_node])
        final_nodes = split_nodes_link(after_images)
        
        expected = [
            TextNode("Welcome to ", TextType.TEXT),
            TextNode("GitHub", TextType.LINK, "https://github.com"),
            TextNode(" check out this ", TextType.TEXT),
            TextNode("icon", TextType.IMAGE, "icon.png"),
            TextNode(" file", TextType.TEXT)
        ]
        self.assertListEqual(final_nodes, expected)


if __name__ == "__main__":
    unittest.main()