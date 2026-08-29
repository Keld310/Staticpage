import unittest
from markdown_blocks import markdown_to_blocks, BlockType, block_to_block_type, markdown_to_html_node

class TestBlockMarkdown(unittest.TestCase):
    def test_markdown_to_blocks_basic(self):
        """Test splitting a normal markdown file into distinct structural blocks."""
        md = "# Heading\n\nThis is a paragraph.\n\n* Item 1\n* Item 2"
        expected = [
            "# Heading",
            "This is a paragraph.",
            "* Item 1\n* Item 2"
        ]
        self.assertListEqual(markdown_to_blocks(md), expected)

    def test_markdown_to_blocks_excessive_newlines(self):
        """Verify that multiple consecutive blank blocks are completely removed."""
        md = "# Heading\n\n\n\nThis is a paragraph.\n\n\n\n\n"
        expected = [
            "# Heading",
            "This is a paragraph."
        ]
        self.assertListEqual(markdown_to_blocks(md), expected)

    def test_markdown_to_blocks_stripping(self):
        """Ensure spaces and tabs at the edges of blocks are stripped off."""
        md = "   # Heading with leading spaces   \n\nParagraph text\n\n"
        expected = [
            "# Heading with leading spaces",
            "Paragraph text"
        ]
        self.assertListEqual(markdown_to_blocks(md), expected)


class TestBlockClassifier(unittest.TestCase):
    def test_classify_heading(self):
        self.assertEqual(block_to_block_type("# Main Title"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("### Small Subheading"), BlockType.HEADING)
        # Missing space after hash makes it a plain text paragraph
        self.assertEqual(block_to_block_type("#NoSpaceHeading"), BlockType.PARAGRAPH)

    def test_classify_code(self):
        code_block = "```\nprint('hello world')\n```"
        self.assertEqual(block_to_block_type(code_block), BlockType.CODE)

    def test_classify_quote(self):
        quote_block = "> First line text\n> Second line text"
        self.assertEqual(block_to_block_type(quote_block), BlockType.QUOTE)
        
        # Missing angle bracket on second line drops structural matching
        bad_quote = "> First line text\nSecond line text missing bracket"
        self.assertEqual(block_to_block_type(bad_quote), BlockType.PARAGRAPH)

    def test_classify_lists(self):
        ul = "* Item Alpha\n* Item Beta"
        self.assertEqual(block_to_block_type(ul), BlockType.UNORDERED_LIST)

        ol = "1. First thing\n2. Second thing\n3. Third thing"
        self.assertEqual(block_to_block_type(ol), BlockType.ORDERED_LIST)

        # Broken numerical step sequence forces standard fallback handling
        bad_ol = "1. First thing\n3. Wrong sequence index step"
        self.assertEqual(block_to_block_type(bad_ol), BlockType.PARAGRAPH)

class TestMarkdownToHTMLNode(unittest.TestCase):
    def test_markdown_to_html_paragraph(self):
        """Verify standard text blocks parse into basic paragraph HTML tags."""
        md = "This is a simple paragraph with some text."
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><p>This is a simple paragraph with some text.</p></div>")

    def test_markdown_to_html_heading(self):
        """Verify diverse level headers translate to structural h1-h6 tags."""
        md = "# Main Header\n\n### Sub Header"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><h1>Main Header</h1><h3>Sub Header</h3></div>")

    def test_markdown_to_html_code_block(self):
        """Ensure code blocks preserve code structures verbatim without tokenizing nested markers."""
        md = "```\ndef my_func():\n    print('**bold test**')\n```"
        node = markdown_to_html_node(md)
        html = node.to_html()
        # Verifies the content inside code stays literal and is wrapped in pre/code tags
        expected = "<div><pre><code>def my_func():\n    print('**bold test**')</code></pre></div>"
        self.assertEqual(html, expected)

    def test_markdown_to_html_blockquote(self):
        """Verify blockquotes strip structural angle tags and nest children elements."""
        md = "> This is a blockquote line.\n> This is another line."
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><blockquote>This is a blockquote line. This is another line.</blockquote></div>")

    def test_markdown_to_html_lists(self):
        """Verify lists map line steps accurately to lists of individual li elements."""
        md = "* Item A\n* Item B\n\n1. Step One\n2. Step Two"
        node = markdown_to_html_node(md)
        html = node.to_html()
        
        expected = (
            "<div>"
            "<ul><li>Item A</li><li>Item B</li></ul>"
            "<ol><li>Step One</li><li>Step Two</li></ol>"
            "</div>"
        )
        self.assertEqual(html, expected)

    def test_markdown_to_html_with_inline_formatting(self):
        """Ensure mixed inline formatting (like bolding and links) resolves correctly within blocks."""
        md = "This has **bold** text and a [link](https://boot.dev)."
        node = markdown_to_html_node(md)
        html = node.to_html()
        
        expected = '<div><p>This has <b>bold</b> text and a <a href="https://boot.dev">link</a>.</p></div>'
        self.assertEqual(html, expected)


if __name__ == "__main__":
    unittest.main()
