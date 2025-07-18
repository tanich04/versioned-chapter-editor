import chromadb
import os
import re
from datetime import datetime

client = chromadb.PersistentClient(path=".chroma_storage")
collection = client.get_or_create_collection("chapter_versions")

def save_version(version_name, content, tags):
    try:
        metadata = {
            "tags": ", ".join([t.strip() for t in tags]),
            "created_at": datetime.now().isoformat()
        }
        collection.add(
            documents=[content],
            ids=[version_name],
            metadatas=[metadata]
        )
        print(f"✅ Version '{version_name}' saved with tags {metadata['tags']} at {metadata['created_at']}")
    except Exception as e:
        print(f"❌ Failed to save version: {e}")

def search_versions(query):
    return collection.query(query_texts=[query], n_results=3)

def get_all_versions():
    all_data = collection.get()
    for i, version_id in enumerate(all_data["ids"]):
        metadata = all_data["metadatas"][i]
        print(f"📄 {version_id} | Tags: {metadata.get('tags', '')} | Created: {metadata.get('created_at', 'N/A')}")
    return all_data

def generate_new_version_id(base_filename):
    """
    Generates a new version ID like `chapter1_final_v2.txt` based on existing versions in chroma.
    """
    name, ext = os.path.splitext(base_filename)
    counter = 1
    existing_versions = collection.get()["ids"]
    while f"{name}_final_v{counter}{ext}" in existing_versions:
        counter += 1
    return f"{name}_final_v{counter}{ext}"
