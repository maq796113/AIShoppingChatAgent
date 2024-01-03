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
generation_config = {
  "temperature": 0,
  "top_p": 1,
  "top_k": 1,
  "max_output_tokens": 2048,
}
 
safety_settings = [
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  }
]
model = genai.GenerativeModel(model_name="gemini-pro",
                              generation_config=generation_config,
                              safety_settings=safety_settings)

st.title("AI Search Agent")
text_search = st.text_input("Search videos by title or speaker", value="")

response : str = ''

col1, col2 = st.columns(2)

def click_button():
    clicked = True

if text_search:
    # get_data(text_search)
    
    with open('results.json') as json_file:
        json_data = json.load(json_file)
    
    # if(json_data):
    #     prompt = f"Give me title,link,price and thumbnail from {json_data['shopping_results']}"
    #     response = model.generate_content(
    #         prompt,
    #         stream=True,
    #         generation_config=generation_config)

    # chatbot = []
    # for chunk in response:
    #     for i in range(0,len(chunk.text),10):
    #         chatbot.append(chunk.text)
    # if clicked == True:
    for item in json_data['shopping_results'][:5]:
        with st.container(): 
          st.text(item['title'])
          st.image(item['thumbnail'],width=100)
          st.link_button('Product Market : ' + item['source'],item['link'])
          st.text('Price : ' + item['price'])
          st.divider()
    st.button('load more...',on_click=click_button)