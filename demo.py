from serpapi import GoogleSearch
import os
import time
import uuid
import json
import streamlit as st
import google.generativeai as genai

from dotenv import load_dotenv

load_dotenv()

GOOGLE_API_KEY = os.environ.get('API')
SEARCH_API = os.environ.get('SEARCH_API')

print("google-generativeai:", genai.__version__)

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

google_key = GOOGLE_API_KEY
if not google_key:
    raise ValueError(
        "GOOGLE_API_KEY is not set. "
        "Please follow the instructions in the README to set it up.")

genai.configure(api_key=google_key)
generation_config = genai.types.GenerationConfig(
        temperature=0.4,
        max_output_tokens=1024,
        top_k=4,
        top_p=1)

model = genai.GenerativeModel('gemini-pro')

st.title("AI Search Agent")
text_search = st.text_input("Search videos by title or speaker", value="")

if text_search:
    get_data(text_search)
    
    with open('results.json') as json_file:
        json_data = json.load(json_file)
    
    if(json_data):
        prompt = f"Give me top 4 from this json : {json_data['shopping_results']}"
        print(prompt)
        response = model.generate_content(
            prompt,
            stream=True,
            generation_config=generation_config)
        
        chatbot = ""
        for chunk in response:
            for i in range(0, len(chunk.text), 10):
                section = chunk.text[i:i + 10]
                chatbot += section
                # time.sleep(0.01)
        st.text(chatbot)
