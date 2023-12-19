import os
import time
from PIL import Image


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

# for Text

messages = "Make search query for Google Search online in amazon about : large size t-shirt"

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

# get_response(response)


# for Images
IMAGE_WIDTH = 512
file = 'test.png'
text_prompt = "Make search query for this clothes in Google Search online with amazon\n"

def preprocess_image(image):
    image_height = int(image.height * IMAGE_WIDTH / image.width)
    return image.resize((IMAGE_WIDTH, image_height))

image = Image.open(file).convert('RGB')
image = preprocess_image(image)

image_prompt = Image.open(file).convert('RGB')
model = genai.GenerativeModel('gemini-pro-vision')


prompt_parts = [
  text_prompt,
  image,
]

response = model.generate_content(
    prompt_parts,
    stream=True,
    generation_config=generation_config
)

get_response(response)
