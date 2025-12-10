from pinecone import Pinecone,SearchQuery,SearchRerank
from gemini_response import *


pc = Pinecone(api_key="pcsk_6g3cAn_T7qTFzj7v1BWKHKVSEceNtZrbM7cjRuUjHXyYdSh9hCum8iqAKd1T1gTZpzQpPs") #Add your own API key

index_name = "pinecone-client-testing"

dense_index = pc.Index(name=index_name)

#Displays the details of the index
# stats = dense_index.describe_index_stats()
# print(stats)


def print_results(search_results):
    for hit in search_results['result']['hits']:
        print(f"id: {hit['_id']:<5} | score: {round(hit['_score'], 3):<5} | text:\n {hit['fields']['chunk_text']:<50}")


# Define the query
query = input("Enter your question....")

# Search the dense index
results = dense_index.search(
    namespace="testing1-namespace",
    query=SearchQuery(
        top_k=1,
        inputs={'text': query}
    )
)

# print_results(results)

generate_answer(query,results)