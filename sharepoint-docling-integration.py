import requests
import os
from pathlib import Path
from azure.identity import ClientSecretCredential
from docling.document_converter import DocumentConverter
from docling.chunking import HybridChunker
from App.chunking import chunk_document,analyze_chunks,save_chunks
from transformers import AutoTokenizer

# --- 1. Processing Logic (From your Chunking Script) ---

def process_and_chunk(download_url: str, file_name: str, max_tokens: int = 512):
    """Parses a remote SharePoint file and applies Hybrid Chunking."""
    print(f"\n🚀 Processing Cloud File: {file_name}")

    try:
        # Step 1: Convert document (Docling accepts URLs directly)
        print("   Step 1: Converting document...")
        converter = DocumentConverter()
        result = converter.convert(download_url)
        doc = result.document

        # Step 2: Initialize tokenizer
        print("   Step 2: Initializing tokenizer...")
        model_id = "sentence-transformers/all-MiniLM-L6-v2"
        tokenizer = AutoTokenizer.from_pretrained(model_id)

        # Step 3: Create HybridChunker
        print(f"   Step 3: Creating chunker (max {max_tokens} tokens)...")
        chunker = HybridChunker(
            tokenizer=tokenizer,
            max_tokens=max_tokens,
            merge_peers=True
        )

        # Step 4: Generate chunks
        print("   Step 4: Generating chunks...")
        chunk_iter = chunker.chunk(dl_doc=doc)
        chunks = list(chunk_iter)

        print(f"✅ Created {len(chunks)} chunks for {file_name}")
        
        # --- At this point, you can loop through 'chunks' to upsert to Pinecone ---
        # for chunk in chunks:
        #     context_text = chunker.contextualize(chunk)
        #     # upsert_to_pinecone(context_text, metadata)

        return chunks

    except Exception as e:
        print(f"❌ Error processing {file_name}: {e}")
        return []

# --- 2. SharePoint Crawler Logic ---

def run_sharepoint_sync():
    ALLOWED_EXTENSIONS = ('.pdf', '.xlsx', '.docx')
    
    # Configuration
    tenant_id = os.getenv("TENANT_ID")
    client_id = os.getenv("CLIENT_ID")
    client_secret = os.getenv("CLIENT_SECRET")
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
                        chunks, tokenizer, chunker = chunk_document(download_url)
                else:
                    print(f"⏩ Skipping (Invalid Format): {file_name}")

    # Start the crawl
    print("=" * 60)
    print("STARTING SHAREPOINT TO DOCLING SYNC")
    print("=" * 60)
    walk_and_process(parent_folder_path)

if __name__ == "__main__":
    run_sharepoint_sync()