import unittest
from unittest.mock import patch, mock_open, MagicMock, call
import json
import os
import logging
import sys

# Add the src directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from data_aggregator import DataAggregator

class TestDataAggregator(unittest.TestCase):

    @patch('builtins.open', new_callable=mock_open, read_data='search_name')
    @patch('os.path.exists', return_value=True)
    @patch('os.path.getsize', return_value=10)
    def test_read_search_name(self, mock_exists, mock_getsize, mock_open):
        aggregator = DataAggregator('data/data.json')
        search_name = aggregator.read_search_name()
        self.assertEqual(search_name, 'search_name')

    @patch('builtins.open', new_callable=mock_open, read_data='{}')
    @patch('os.path.exists', return_value=True)
    @patch('os.path.getsize', return_value=10)
    def test_read_found_data(self, mock_exists, mock_getsize, mock_open):
        aggregator = DataAggregator('data/data.json')
        found_data = aggregator.read_found_data()
        self.assertEqual(found_data, {})

    @patch('builtins.open', new_callable=mock_open)
    def test_write_found_data(self, mock_open):
        aggregator = DataAggregator('data/data.json')
        data = {'key': 'value'}
        aggregator.write_found_data(data)
        expected_calls = [
            call('{'),
            call('\n    '),
            call('"key"'),
            call(': '),
            call('"value"'),
            call('\n'),
            call('}')
        ]
        mock_open().write.assert_has_calls(expected_calls, any_order=False)

    @patch('builtins.open', new_callable=mock_open)
    def test_append_links_to_file(self, mock_open):
        aggregator = DataAggregator('data/data.json')
        links = ['https://example.com', 'http://example.org', 'www.example.net', 'example.com']
        aggregator.append_links_to_file(links)
        expected_calls = [
            call('\nsite:https://example.com'),
            call('\nsite:http://example.org'),
            call('\nsite:www.example.net')
        ]
        mock_open().write.assert_has_calls(expected_calls, any_order=True)

    @patch('builtins.open', new_callable=mock_open, read_data='search_name')
    @patch('os.path.exists', return_value=True)
    @patch('os.path.getsize', return_value=10)
    @patch('data_aggregator.DataAggregator.read_found_data', return_value={})
    @patch('data_aggregator.DataAggregator.write_found_data')
    def test_add_found_data(self, mock_write_found_data, mock_read_found_data, mock_exists, mock_getsize, mock_open):
        aggregator = DataAggregator('data/data.json')
        query_data = {'query': 'example_query'}
        links = ['https://example.com']
        updated_data = aggregator.add_found_data(query_data, links)
        self.assertIn('search_name', updated_data)
        self.assertEqual(updated_data['search_name'], links)

    @patch('builtins.open', new_callable=mock_open, read_data='')
    @patch('os.path.exists', return_value=True)
    @patch('os.path.getsize', return_value=0)
    def test_read_search_name_empty(self, mock_exists, mock_getsize, mock_open):
        aggregator = DataAggregator('data/data.json')
        search_name = aggregator.read_search_name()
        self.assertIsNone(search_name)

    @patch('builtins.open', new_callable=mock_open, read_data='{}')
    @patch('os.path.exists', return_value=True)
    @patch('os.path.getsize', return_value=10)
    @patch('data_aggregator.DataAggregator.read_search_name', return_value=None)
    def test_add_found_data_no_search_name(self, mock_read_search_name, mock_exists, mock_getsize, mock_open):
        aggregator = DataAggregator('data/data.json')
        query_data = {'query': 'example_query'}
        links = ['https://example.com']
        with self.assertLogs(level='ERROR') as log:
            updated_data = aggregator.add_found_data(query_data, links)
            self.assertIn("Search name file is empty or does not exist.", log.output[0])
        self.assertEqual(updated_data, {})

if __name__ == '__main__':
    unittest.main()
