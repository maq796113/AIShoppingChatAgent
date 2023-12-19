import os
import time

import google.generativeai as genai
# import weaviate
from llama_index import VectorStoreIndex, SimpleDirectoryReader
# from typing import List, Tuple, Optional, Dict, Union


print("google-generativeai:", genai.__version__)

GOOGLE_API_KEY = os.environ.get('API')

if not GOOGLE_API_KEY:
    raise ValueError(
        "GOOGLE_API_KEY is not set. "
        "Please follow the instructions in the README to set it up.")

# this means the messages could be a string of tuple of tuple strings
# CHAT_HISTORY = List[Tuple[Optional[Union[Tuple[str], str]], Optional[str]]]

genai.configure(api_key=GOOGLE_API_KEY)

generation_config = genai.types.GenerationConfig(
    temperature=0.4,
    max_output_tokens=1024,
    stop_sequences="",
    top_k=32,
    top_p=1
)

messages = "Make search query online about : large size t-shirt"

# preprocess_chat_history(chatbot)

model = genai.GenerativeModel('gemini-pro')
response = model.generate_content(
    messages,
    stream=True,
    generation_config=generation_config
)

def get_response(res):
    chatbot = ""
    for chunk in res:
        for i in range(0, len(chunk.text), 10):
            section = chunk.text[i:i + 10]
            chatbot += section
            time.sleep(0.01)
            # yield chatbot
    print(chatbot)

get_response(response)

