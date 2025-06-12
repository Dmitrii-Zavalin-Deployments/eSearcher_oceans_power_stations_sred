import unittest
from unittest.mock import patch, mock_open
from src.query_builder import QueryBuilder

class TestQueryBuilder(unittest.TestCase):

    @patch('os.getenv', return_value='5')
    @patch('builtins.open', new_callable=mock_open, read_data='Test1\nTest2')
    def test_initialization(self, mock_file, mock_getenv):
        qb = QueryBuilder(10)
        self.assertEqual(qb.run_number, 5)
        self.assertEqual(qb.query_folder, 5 % 10)
        self.assertEqual(qb.all_words, ['Test1', 'Test2'])
        self.assertEqual(qb.exact_phrase, ['Test1', 'Test2'])
        self.assertEqual(qb.any_words, ['Test1', 'Test2'])
        self.assertEqual(qb.none_words, ['Test1', 'Test2'])
        self.assertEqual(qb.domain, ['Test1', 'Test2'])
        self.assertEqual(qb.file_type, ['Test1', 'Test2'])

    @patch('builtins.open', new_callable=mock_open, read_data='Test1\nTest2')
    def test_build_query_all_fields(self, mock_file):
        qb = QueryBuilder(10)
        qb.all_words = ['Test1']
        qb.exact_phrase = ['Test2', 'Test3']
        qb.any_words = ['Test4']
        qb.none_words = ['Test5']
        qb.domain = ['*.com']
        qb.file_type = ['pdf']
        query = qb.build_query()
        self.assertEqual(query, 'Test1 "Test2 Test3" Test4 -Test5 site:*.com filetype:pdf')

    @patch('builtins.open', new_callable=mock_open, read_data='Test1\nTest2')
    def test_build_query_missing_fields(self, mock_file):
        qb = QueryBuilder(10)
        qb.all_words = ['Test1']
        qb.exact_phrase = ['Test2', 'Test3']
        qb.any_words = ['Test4']
        qb.none_words = ['Test5']
        qb.domain = []
        qb.file_type = []
        query = qb.build_query()
        self.assertEqual(query, 'Test1 "Test2 Test3" Test4 -Test5')

    @patch('builtins.open', new_callable=mock_open, read_data='Test1\nTest2')
    def test_load_search_terms_file_not_found(self, mock_file):
        mock_file.side_effect = FileNotFoundError
        qb = QueryBuilder(10)
        terms = qb.load_search_terms('non_existent_file.txt')
        self.assertEqual(terms, [])

    @patch('builtins.open', new_callable=mock_open, read_data='Test1\nTest2')
    def test_get_query_data(self, mock_file):
        qb = QueryBuilder(10)
        query_data = qb.get_query_data()
        self.assertIn('query', query_data)
        self.assertIsInstance(query_data['query'], str)

if __name__ == '__main__':
    unittest.main()
