import requests
from azure.identity import ClientSecretCredential
import os

def list_all_files_recursively():
    Download_url_list=[]
    ALLOWED_EXTENSIONS = ('.pdf', '.xlsx', '.docx')
    # --- Configuration ---
    tenant_id = os.getenv("TENANT_ID")
    client_id = os.getenv("CLIENT_ID")
    client_secret = os.getenv("CLIENT_SECRET")

    site_address = "jivisolutionscom.sharepoint.com:/sites/JIVIManualAndDocuments"
    # Starting point: The parent "Manuals" folder
    parent_folder_path = "User Manuals/Manuals" 

    # 1. Authenticate
    credential = ClientSecretCredential(tenant_id, client_id, client_secret) #type: ignore
    token = credential.get_token("https://graph.microsoft.com/.default")
    headers = {"Authorization": f"Bearer {token.token}"}

    # 2. Get Site ID
    site_url = f"https://graph.microsoft.com/v1.0/sites/{site_address}"
    site_id = requests.get(site_url, headers=headers).json()["id"]

    # 3. Define the Recursive Function
    def walk_folder(current_path):
        print(f"\n📂 Checking Folder: {current_path}")
        
        # Build the URL for the current folder's children
        url = f"https://graph.microsoft.com/v1.0/sites/{site_id}/drive/root:/{current_path}:/children"
        response = requests.get(url, headers=headers).json()
        
        items = response.get("value", [])
        
        for item in items:
            if "file" in item:
                file_name=item['name'].lower()
                if file_name.endswith(ALLOWED_EXTENSIONS):
                    # It's a valid file - print it
                    print(f"  📄 File: {item['name']} (ID: {item['id']})")
                    download_url = item.get('@microsoft.graph.downloadUrl')
                    Download_url_list.append(download_url)
                else:
                    print(f"FILE REJECTED.......INVALID FORMAT:{item['name']}")
            elif "folder" in item:
                # It's a subfolder - get its path and go deeper
                # We construct the new path by joining the current path and folder name
                subfolder_path = f"{current_path}/{item['name']}"
                walk_folder(subfolder_path)

    # Start the process
    print(f"Starting crawl from: {parent_folder_path}")
    print("-" * 50)
    walk_folder(parent_folder_path)
    return Download_url_list

if __name__ == "__main__":
    a=list_all_files_recursively()
    for link in a:
        print(link)