from serpapi import GoogleSearch
import os
import time
import uuid
import json
import streamlit as st
import google.generativeai as genai
from PIL import Image

from dotenv import load_dotenv

load_dotenv()

GOOGLE_API_KEY = os.environ.get('API')
SEARCH_API = os.environ.get('SEARCH_API')

print("google-generativeai:", genai.__version__)

def get_data(keyword: str):
    
    prompt = f"Give me search prompt for this description online : {keyword}"
    response = model.generate_content(
        prompt,
        stream=True,
        generation_config=generation_config)
    
    try:
      response.resolve()
      params = {
          "api_key": SEARCH_API,
          "engine": "google_shopping",
          "q": str(response.text),
          "google_domain": "google.com"
      }
      search = GoogleSearch(params)
      results = search.get_dict()
      json.dump(results, open('results.json', 'w'), indent=2)
    except Exception as e:
      print(f'{type(e).__name__}: {e}')


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

container = st.container()
text_search = container.text_input("Search by text", value="")
upload_button = container.text("Or")
upload_file = container.file_uploader("Upload Image",type=["png","jpg","jpeg"])
response : str = ''

page = 5

json_data = ''

def click_button():
    page += 5
    for item in json_data['shopping_results'][page:page+5]:
        card(item)

def card(data):
  with st.container(): 
      st.text(data['title'])
      st.image(data['thumbnail'],width=100)
      st.link_button('Product Market : ' + data['source'],data['link'])
      st.text('Price : ' + data['price'])
      st.divider()

if text_search:
    get_data(text_search)
    
    results_container = st.container()
        
    with open('results.json') as json_file:
      json_data = json.load(json_file)
      
    if(json_data):
        print(json_data['shopping_results'])
    
        for item in json_data['shopping_results'][:page]:
            card(item)
        
        if st.button("Add More Results"):   
            page += 5
            for item in json_data['shopping_results'][page:page+5]:
                with results_container:
                  card(item)
if upload_file:
  st.write('upload succeed')
  img = Image.open(upload_file).convert('RGB')
  st.image(img)