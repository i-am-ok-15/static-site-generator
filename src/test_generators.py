import unittest

from generators import extract_title

class TestGenerators(unittest.TestCase):

    def test_extract_title_expected(self):

        markdown = "# Hello World"
        result = extract_title(markdown)
        self.assertEqual(result, "Hello World")

    def test_extract_title_trialing(self):

        markdown = "# Hello World       #"
        result = extract_title(markdown)
        self.assertEqual(result, "Hello World")

    def test_extract_title_extra_leading(self):

        markdown = "#    Hello World"
        result = extract_title(markdown)
        self.assertEqual(result, "Hello World")

    def test_extract_title_double_title(self):

        markdown = """# Hello World
        # This is not the title"""
        result = extract_title(markdown)
        self.assertEqual(result, "Hello World")