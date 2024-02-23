# -*- coding: utf-8 -*-

"""
File: client.py
Author: Dartrisen
Description: tests.
"""
import unittest
from unittest.mock import patch

from groq.client import Client


class TestClient(unittest.TestCase):
    """Test class."""
    def test_create_chat(self):
        # Mocking requests.post to avoid actual HTTP requests
        with patch('requests.post') as mock_post:
            mock_post.return_value.iter_lines.return_value = [
                '{"result": {'
                '"content": "Test response", '
                '"requestId": "123456", '
                '"stats": {'
                '"timeGenerated": 10, '
                '"tokensGenerated": 20, '
                '"timeProcessed": 5, '
                '"tokensProcessed": 15'
                '}}}'
            ]
            client = Client()
            chat = client.create_chat("Test prompt")
            self.assertEqual(chat.content, "Test response")
            self.assertEqual(chat.request_id, "123456")
            self.assertEqual(chat.stats.time_generated, 10)
            self.assertEqual(chat.stats.tokens_generated, 20)
            self.assertEqual(chat.stats.time_processed, 5)
            self.assertEqual(chat.stats.tokens_processed, 15)

    def test_create_chat_with_history(self):
        with patch('requests.post') as mock_post:
            mock_post.return_value.iter_lines.return_value = [
                '{"result": {'
                '"content": "Test response with history", '
                '"requestId": "789012", '
                '"stats": {'
                '"timeGenerated": 20, '
                '"tokensGenerated": 30, '
                '"timeProcessed": 10, '
                '"tokensProcessed": 25'
                '}}}'
            ]

            client = Client()
            chat = client.create_chat("Test prompt with history", history=["previous message"])
            self.assertEqual(chat.content, "Test response with history")
            self.assertEqual(chat.request_id, "789012")
            self.assertEqual(chat.stats.time_generated, 20)
            self.assertEqual(chat.stats.tokens_generated, 30)
            self.assertEqual(chat.stats.time_processed, 10)
            self.assertEqual(chat.stats.tokens_processed, 25)


if __name__ == '__main__':
    unittest.main()
