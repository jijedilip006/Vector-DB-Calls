from pinecone import Pinecone,SearchQuery,SearchRerank


pc = Pinecone(api_key="") #Add your own API key

index_name = "pinecone-client-testing"

dense_index = pc.Index(name=index_name)

#Displays the details of the index
# stats = dense_index.describe_index_stats()
# print(stats)


def print_results(search_results):
    for hit in search_results['result']['hits']:
        print(f"id: {hit['_id']:<5} | score: {round(hit['_score'], 3):<5} | category: {hit['fields']['category']:<10} | text: {hit['fields']['chunk_text']:<50}")


# Define the query
query = "Famous historical structures and monuments"

# Search the dense index
results = dense_index.search(
    namespace="testing-namespace",
    query=SearchQuery(
        top_k=10,
        inputs={'text': query}
    )
)

print_results(results)