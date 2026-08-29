import unittest
from markdown_blocks import markdown_to_blocks

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

if __name__ == "__main__":
    unittest.main()
