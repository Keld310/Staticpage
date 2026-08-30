import unittest
from gencontent import extract_title


# Assuming your function is in a file named formula or imported above
# from your_script import extract_title

class TestExtractTitle(unittest.TestCase):
    
    def test_standard_h1(self):
        """Test a clean, standard H1 header."""
        markdown = "# Hello"
        self.assertEqual(extract_title(markdown), "Hello")

    def test_whitespace_stripping(self):
        """Test that extra whitespace around the hash and title is stripped."""
        markdown = "   #    Hello World   "
        self.assertEqual(extract_title(markdown), "Hello World")

    def test_multiline_markdown(self):
        """Test extracting the H1 when it is surrounded by other text blocks."""
        markdown = (
            "This is an intro paragraph.\n"
            "# My Main Title\n"
            "Some more text content down here."
        )
        self.assertEqual(extract_title(markdown), "My Main Title")

    def test_missing_h1_raises_exception(self):
        """Test that a ValueError is raised if no H1 header is present."""
        markdown = "## This is an H2 header\nJust some text."
        with self.assertRaises(ValueError):
            extract_title(markdown)

    def test_invalid_h1_no_space(self):
        """Test that a line starting with '#' but no space raises an exception."""
        markdown = "#Hello Without Space"
        with self.assertRaises(ValueError):
            extract_title(markdown)

if __name__ == "__main__":
    unittest.main()