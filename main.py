import os
from pinecone import Pinecone

api_key=os.getenv("PINECONE_API_KEY")

pc = Pinecone(api_key=api_key)

