from pinecone import Pinecone
import pymupdf as fitz
from chunking import chunk_document, analyze_chunks, save_chunks
pc = Pinecone(api_key="pcsk_6g3cAn_T7qTFzj7v1BWKHKVSEceNtZrbM7cjRuUjHXyYdSh9hCum8iqAKd1T1gTZpzQpPs") #add your own API key
pdf_path="Training manual -Employee profile.pdf"
max_tokens=2048
output_path="output.txt"
try:
    chunks, tokenizer, chunker = chunk_document(pdf_path, max_tokens)
    record=save_chunks(chunks,chunker,output_path)
    # print(record)
except Exception as e:
    print(e)

records=[]
for id,chunk in record:
    records.append({"_id":"rec"+str(id),"chunk_text":chunk})

    

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
print("Successfully upserted")

