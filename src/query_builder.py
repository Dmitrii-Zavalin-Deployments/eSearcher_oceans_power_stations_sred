import os
import json

class QueryBuilder:
    def __init__(self, NUMBER_OF_QUERIES):
        self.run_number = int(os.getenv('GITHUB_RUN_NUMBER', 0))
        self.query_folder = self.run_number % NUMBER_OF_QUERIES
        print(f'GitHub Actions Run Number: {self.run_number}')
        print(f'Number of Queries: {NUMBER_OF_QUERIES}')
        print(f'Query Folder: {self.query_folder}')
        
        # Load search terms from files
        self.all_words = self.load_search_terms(f'data/{self.query_folder}/all_words.txt')
        self.exact_phrase = self.load_search_terms(f'data/{self.query_folder}/exact_phrase.txt')
        self.any_words = self.load_search_terms(f'data/{self.query_folder}/any_words.txt')
        self.none_words = self.load_search_terms(f'data/{self.query_folder}/none_words.txt')
        self.domain = self.load_search_terms(f'data/{self.query_folder}/domain.txt')
        self.file_type = self.load_search_terms(f'data/{self.query_folder}/file_type.txt')

    def build_query(self):
        query_parts = []

        if self.all_words:
            query_parts.append(' '.join(self.all_words))
        if self.exact_phrase:
            query_parts.append(f'"{" ".join(self.exact_phrase)}"')
        if self.any_words:
            query_parts.append(' '.join(self.any_words))
        if self.none_words:
            query_parts.append(' '.join(f'-{word}' for word in self.none_words))
        if self.domain:
            query_parts.append(f'site:{self.domain[0]}')
        if self.file_type:
            query_parts.append(f'filetype:{self.file_type[0]}')

        return ' '.join(query_parts)

    def get_query_data(self):
        return {
            "query": self.build_query()
        }

    def load_search_terms(self, file_path):
        try:
            with open(file_path, 'r') as file:
                terms = file.read().splitlines()
            return terms
        except FileNotFoundError:
            print(f"The file {file_path} was not found.")
            return []
