#Here we can test to the GenAI API to make sure it is generating the book summaries correctly
import unittest
from unittest.mock import patch, MagicMock
from app.genai import generate_summary

class TestGenAISummary(unittest.TestCase):

    @patch('app.genai.client.models.generate_content')
    def test_generate_summary(self, mock_generate_content):
        # Setup fake response
        mock_response = MagicMock()
        mock_response.text = "This is a mock summary."
        mock_generate_content.return_value = mock_response

        summary = generate_summary("The Hobbit", "J.R.R. Tolkien")

        mock_generate_content.assert_called_once_with(
            model='gemini-2.5-flash',
            contents="Generate a 1-3 sentence summary of the book The Hobbit by J.R.R. Tolkien"
        )

        self.assertEqual(summary, "This is a mock summary.")
 
    @patch('app.genai.client.models.generate_content')
    def test_long_title_and_author(self, mock_generate_content):
        mock_response = MagicMock()
        mock_response.text = "This is a summary for a long book title."
        mock_generate_content.return_value = mock_response

        long_title = "A Very Extremely Long Book Title That Might Break Things Because It's Way Too Verbose"
        long_author = "A Ridiculously Long Author Name That Barely Fits On a Book Cover"
        summary = generate_summary(long_title, long_author)
        self.assertIn("summary", summary.lower())
