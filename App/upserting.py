from pinecone import Pinecone
import pymupdf as fitz
from chunking import chunk_document, analyze_chunks, save_chunks
pc = Pinecone(api_key="pcsk_6g3cAn_T7qTFzj7v1BWKHKVSEceNtZrbM7cjRuUjHXyYdSh9hCum8iqAKd1T1gTZpzQpPs") #add your own API key
pdf_paths=["Training manual -Employee profile.pdf","Training manual -Roster group Assignment.pdf","Training Manual -Workload Planner.pdf","Training Manual- Roster Creation & Employee Roster.pdf","Training Manual-Final Booking Report.pdf","Training Manual-HSSE Planning.pdf","Training Manual-Lashing Deployment.pdf","Training Manual-Maritime Setup.pdf","Training Manual-Prime Mover Planning.pdf","Training Manual-RTG planning.pdf","Training Manual-Stackers Planning.pdf","Training Manual-System Definitions.pdf","Training Manual-Time and Attendance.pdf","Training Manual-Workforce Execution.pdf"]
max_tokens=2048
count = 1
output_path="output.txt"
records=[]


index_name = "pinecone-client-testing"
dense_index = pc.Index(name=index_name)
for pdf_path in pdf_paths:
    try:
        chunks, tokenizer, chunker = chunk_document(pdf_path, max_tokens)
        record=save_chunks(chunks,chunker,output_path)
        for id,chunk in record:
            records.append({"_id":"rec"+str(count),"chunk_text":chunk})
            count+=1
            print(count)
        dense_index.upsert_records(namespace="testing2-namespace", records=records)
        print('='*60)
        print("RECORDS HAVE BEEN UPSERTED. RESETTING RECORDS....")
        records=[]
        # print(record)
    except Exception as e:
        print(e)
    
if not pc.has_index(name=index_name):
    pc.create_index_for_model(
        name=index_name,
        cloud='aws',
        region='us-east-1',
        embed={"model":"llama-text-embed-v2","field_map":{"text":"chunk_text"}}  # type: ignore
    )





# dense_index.upsert_records(namespace="testing2-namespace", records=records)
print("Successfully upserted")

