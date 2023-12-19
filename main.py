import os
import google.generativeai as genai
# import weaviate
from llama_index import VectorStoreIndex, SimpleDirectoryReader

api_id = os.environ.get('API_Key')

