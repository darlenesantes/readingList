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
