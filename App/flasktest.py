from flask import Flask, render_template, request, jsonify
from pinecone import Pinecone, SearchQuery
from google import genai
from google.genai import types
import os
from gemini_response import *

app = Flask(__name__)

# --- Configuration ---
PINECONE_KEY = "pcsk_6g3cAn_T7qTFzj7v1BWKHKVSEceNtZrbM7cjRuUjHXyYdSh9hCum8iqAKd1T1gTZpzQpPs"

# Initialize Clients
pc = Pinecone(api_key=PINECONE_KEY)
dense_index = pc.Index("pinecone-client-testing")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    user_query = request.json.get('message')
    
    # Search Pinecone
    results = dense_index.search(
    namespace="testing2-namespace",
    query=SearchQuery(
        top_k=20,
        inputs={'text': user_query}
    )
    )
    
    # Get Gemini Response
    answer = generate_answer(user_query, results)
    
    return jsonify({"response": answer})

if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0",port=80)