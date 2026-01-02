import requests
from pinecone import Pinecone
import os
from pathlib import Path
from azure.identity import ClientSecretCredential
from docling.document_converter import DocumentConverter
from App.chunking import chunk_document,analyze_chunks,save_chunks

# --- 2. SharePoint Crawler Logic ---
def run_sharepoint_sync():
    ALLOWED_EXTENSIONS = ('.pdf', '.xlsx', '.docx')
    pinecone_api_key=os.getenv("PINECONE_API_KEY")
    print(pinecone_api_key)
    pc = Pinecone(api_key=pinecone_api_key)
    index_name = "pinecone-client-testing"
    dense_index = pc.Index(name=index_name)
    global count
    count=1
    # Configuration
    tenant_id = os.getenv("TENANT_ID")
    client_id = os.getenv("CLIENT_ID")
    client_secret = os.getenv("CLIENT_SECRET")
    #Check for environment variables
    print(tenant_id,client_id,client_secret,sep="\n")

    site_address = "jivisolutionscom.sharepoint.com:/sites/JIVIManualAndDocuments"
    parent_folder_path = "User Manuals/Manuals"

    # 1. Authenticate
    credential = ClientSecretCredential(tenant_id, client_id, client_secret) #type: ignore
    token = credential.get_token("https://graph.microsoft.com/.default")
    headers = {"Authorization": f"Bearer {token.token}"}

    # 2. Get Site ID
    site_url = f"https://graph.microsoft.com/v1.0/sites/{site_address}"
    site_id = requests.get(site_url, headers=headers).json()["id"]

    # 3. Recursive Walker
    def walk_and_process(current_path):
        global count
        print(f"\n📂 Entering Folder: {current_path}")
        
        url = f"https://graph.microsoft.com/v1.0/sites/{site_id}/drive/root:/{current_path}:/children"
        response = requests.get(url, headers=headers).json()
        items = response.get("value", [])
        
        for item in items:
            if "folder" in item:
                # Recursive call for subfolders
                subfolder_path = f"{current_path}/{item['name']}"
                walk_and_process(subfolder_path)
                
            elif "file" in item:
                file_name = item['name']
                if file_name.lower().endswith(ALLOWED_EXTENSIONS):
                    download_url = item.get('@microsoft.graph.downloadUrl')
                    if download_url:
                        # TRIGGER DOCLING PIPELINE
                        # process_and_chunk(download_url, file_name)
                        chunks, tokenizer, chunker = chunk_document(download_url,file_name)
                        record=save_chunks(chunks,chunker,"output_sync.txt")
                        records=[]
                        for id,chunk in record:
                            records.append({"_id":"rec"+str(count)+file_name,"chunk_text":chunk})
                            count+=1
                            print(count)
                            if len(records)==96:
                                dense_index.upsert_records(namespace="testing3-namespace", records=records)
                                records=[]
                                print('='*60)
                                print("RECORDS HAVE BEEN UPSERTED. RESETTING RECORDS....")
                        dense_index.upsert_records(namespace="testing3-namespace", records=records)
                        print('='*60)
                        print("RECORDS HAVE BEEN UPSERTED. RESETTING RECORDS....")
                        records=[]
                else:
                    print(f"⏩ Skipping (Invalid Format): {file_name}")

    # Start the crawl
    print("=" * 60)
    print("STARTING SHAREPOINT TO DOCLING SYNC")
    print("=" * 60)
    walk_and_process(parent_folder_path)

if __name__ == "__main__":
    run_sharepoint_sync()