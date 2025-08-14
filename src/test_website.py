from website_functions import (extract_title)
import unittest

class TestWebsite(unittest.TestCase):
    def testExtractTitle(self):
        self.assertEqual(extract_title("""# Header 1
        some other line
        more lines"""),
        "Header 1"
    )
    
if __name__ == "__main__":
    unittest.main()
