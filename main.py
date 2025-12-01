import os
from pinecone import Pinecone

api_key=os.getenv("PINECONE_API_KEY")

pc = Pinecone(api_key=api_key)

index_name = "Pinecone-client-Testing"

if not pc.has_index(name=index_name):
    pc.create_index_for_model(
        name=index_name,
        cloud='aws',
        region='us-east-1',
        embed={"model":"llama-text-embed-v2","field_map":{"text":"chunk_text"}}  # type: ignore
    )

