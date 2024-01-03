from serpapi import GoogleSearch
import os
import time
import uuid
import json
import streamlit as st

from dotenv import load_dotenv

load_dotenv()

GOOGLE_API_KEY = os.environ.get('API')
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


# from google_web_scrappper import get_data
# get_data(prompt_input)
# with open('results.json') as json_file:
#     json_data = json.load(json_file)

text_search = st.text_input("Search videos by title or speaker", value="")

if text_search:
    get_data(text_search)
    
    with open('results.json') as json_file:
        json_data = json.load(json_file)
    
    # print(json_data)
    st.json(json_data)
