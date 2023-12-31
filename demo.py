from serpapi import GoogleSearch
import os
import json
from dotenv import load_dotenv

load_dotenv()

SEARCH_API = os.environ.get('SEARCH_API')

def get_data(keyword: str):
    params = {
        "api_key": SEARCH_API,
        "engine": "google_shopping",
        "q": keyword,
        "google_domain": "google.com"
    }

    search = GoogleSearch(params)
    results = search.get_dict()
    json.dump(results, open('results.json', 'w'), indent=2)
get_data('black hoodie')


# from google_web_scrappper import get_data
# get_data(prompt_input)
# with open('results.json') as json_file:
#                      json_data = json.load(json_file)