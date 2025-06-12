import json
import os
import logging

class DataAggregator:
    def __init__(self, found_file_path):
        self.found_file_path = found_file_path
        self.logger = logging.getLogger(__name__)
        self.run_number = int(os.getenv('GITHUB_RUN_NUMBER', 0))
        self.query_folder = self.run_number % int(os.getenv('NUMBER_OF_QUERIES', 1))
        print(f'GitHub Actions Run Number: {self.run_number}')
        print(f'Number of Queries: {os.getenv("NUMBER_OF_QUERIES", 1)}')
        print(f'Query Folder: {self.query_folder}')

    def append_links_to_file(self, links):
        file_path = f'data/{self.query_folder}/none_words.txt'
        with open(file_path, 'a') as file:
            for link in links:
                # Check if the link starts with "http://", "https://", or "www"
                if link.startswith(("http://", "https://", "www")):
                    file.write('\nsite:' + link)

    def read_found_data(self):
        if os.path.exists(self.found_file_path) and os.path.getsize(self.found_file_path) > 0:
            with open(self.found_file_path, 'r') as file:
                return json.load(file)
        else:
            return {}

    def write_found_data(self, data):
        with open(self.found_file_path, 'w') as file:
            json.dump(data, file, indent=4)

    def read_search_name(self):
        file_path = f'data/{self.query_folder}/search_name.txt'
        if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
            with open(file_path, 'r') as file:
                return file.read().strip()
        else:
            return None

    def add_found_data(self, query_data, links):
        self.append_links_to_file(links)
        found_data = self.read_found_data()
        
        query_key = self.read_search_name()
        if query_key is None:
            self.logger.error("Search name file is empty or does not exist.")
            return found_data

        if query_key not in found_data:
            found_data[query_key] = []

        found_data[query_key].extend(links)
        
        self.write_found_data(found_data)
        return found_data