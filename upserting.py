from pinecone import Pinecone
import pymupdf as fitz

pc = Pinecone(api_key="pcsk_6g3cAn_T7qTFzj7v1BWKHKVSEceNtZrbM7cjRuUjHXyYdSh9hCum8iqAKd1T1gTZpzQpPs") #add your own API key

document = fitz.open("Training manual -Employee profile.pdf")
records = []
count=1
text=''
try:
    for page in document:
        records.append({"_id":"rec"+str(count),"chunk_text":page.get_text()})
        count+=1

finally:
    print(records)

    

index_name = "pinecone-client-testing"

if not pc.has_index(name=index_name):
    pc.create_index_for_model(
        name=index_name,
        cloud='aws',
        region='us-east-1',
        embed={"model":"llama-text-embed-v2","field_map":{"text":"chunk_text"}}  # type: ignore
    )



dense_index = pc.Index(name=index_name)

dense_index.upsert_records(namespace="testing1-namespace", records=records)

