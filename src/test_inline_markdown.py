import unittest
from textnode import TextNode, TextType, text_node_to_html_node
from inline_markdown import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link
class TestInlineMarkdown(unittest.TestCase):
    def test_split_code(self):
        """Test splitting an inline code block."""
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_bold(self):
        """Test splitting a bold string modification sequence."""
        node = TextNode("Hello **bold** world!", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [
            TextNode("Hello ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" world!", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_italic(self):
        """Test splitting an italic phrase."""
        node = TextNode("This is *italicized* text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "*", TextType.ITALIC)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("italicized", TextType.ITALIC),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_unclosed_delimiter_raises_error(self):
        """Test that missing matching closing delimiters raises a ValueError."""
        node = TextNode("This formatting **has no end tag", TextType.TEXT)
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "**", TextType.BOLD)

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
        "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
    )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)


    def test_extract_markdown_images_empty_alt(self):
        """Test finding an image with an empty alt text string."""
        matches = extract_markdown_images(
            "An image with no alt text: ![](https://example.com)"
        )
        self.assertListEqual([("", "https://example.com")], matches)

    def test_extract_markdown_images_ignores_TEXT_links(self):
        """Ensure standard links are ignored by the image parser."""
        matches = extract_markdown_images(
            "This is a plain link [Google](https://google.com) and should be ignored."
        )
        self.assertListEqual([], matches)


    # --- Tests for extract_markdown_links ---

    def test_extract_markdown_links(self):
        """Test finding a standard markdown link."""
        matches = extract_markdown_links(
            "Click here to visit [Boot.dev](https://boot.dev) for courses."
        )
        self.assertListEqual([("Boot.dev", "https://boot.dev")], matches)

    def test_extract_markdown_links_empty_anchor(self):
        """Test finding a link with an empty anchor text string."""
        matches = extract_markdown_links(
            "This link has empty brackets: [](https://boot.dev)"
        )
        self.assertListEqual([("", "https://boot.dev")], matches)

    def test_extract_markdown_links_ignores_images(self):
        """Ensure markdown images are ignored by the link parser via negative lookbehind."""
        matches = extract_markdown_links(
            "This is an image ![sunset](https://example.com) and should be ignored."
        )
        self.assertListEqual([], matches)


    # --- Mixed Content Integration Test ---

    def test_mixed_markdown_content(self):
        """Test both extractors on a block containing a mix of links and images."""
        mixed_text = (
            "Check out [GitHub](https://github.com) or look at this "
            "![avatar](https://example.com) on our homepage."
        )
        
        # Verify link extractor only pulls the link
        self.assertListEqual(
            [("GitHub", "https://github.com")], 
            extract_markdown_links(mixed_text)
        )
        
        # Verify image extractor only pulls the image
        self.assertListEqual(
            [("avatar", "https://example.com")], 
            extract_markdown_images(mixed_text)
        )


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

    def test_text_to_html_TEXT(self):
        """Verify conversion of a TEXT node into a plain LeafNode."""
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

    def test_split_image_ignores_non_TEXT_nodes(self):
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