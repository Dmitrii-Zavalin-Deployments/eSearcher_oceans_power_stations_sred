# eSearcher

## Legal Note

The search service is provided by Google (https://www.google.com) according to these terms and conditions: https://support.google.com/programmable-search/answer/1714300 and these instructions: https://developers.google.com/custom-search/v1/overview

## Link to the search details

https://dmitrii-zavalin-deployments.github.io/eSearcher/information.html

## How to add new search requests

1. Update `.github/workflows/main.yml` (line 14) to increase the number of queries by one.
2. Create a new folder in `data` with the next number (e.g., if folders 0,1,2,3,4 exist, create folder 5).
3. Add the following files to the new folder:
   - `all_words.txt`: "all these words:" from Google Advanced Search
   - `any_words.txt`: "any of these words:" from Google Advanced Search
   - `domain.txt`: "site or domain:" from Google Advanced Search (e.g., *.com)
   - `exact_phrase.txt`: "this exact word or phrase:" from Google Advanced Search
   - `none_words.txt`: "none of these words:" from Google Advanced Search
   - `file_type.txt`: "file type:" from Google Advanced Search (e.g., pdf)
   - `search_name.txt`: Name for this search (appears in information.html)