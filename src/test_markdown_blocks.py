import unittest
from markdown_blocks import markdown_to_blocks, BlockType, block_to_block_type

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

if __name__ == "__main__":
    unittest.main()
