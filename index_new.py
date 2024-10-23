from elasticsearch import Elasticsearch
import os
import json
from constants import *

# Connect to Elasticsearch
es = Elasticsearch(
    "http://localhost:9200/"
)
print(es.info())
ERR_FILES = 0
TOTAL_FILES = 0
def index_document(filepath):
    global ERR_FILES, TOTAL_FILES
    TOTAL_FILES += 1
    try:
        # print(filepath)
        with open(filepath, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Extract filename as title
        title = os.path.basename(filepath)
        # print(content, '\n\n\n')
        # print(os.path.join(os.getcwd(), filepath));
        # Index the document
        es.index(index="myntra", body={
            "title": title,
            "content": content,
            "path": os.path.join(os.getcwd(), filepath)
        })

    except Exception as e:
        print(f"Error processing {filepath}: {e}")
        ERR_FILES += 1

# Directory containing your documents
docs_dir = "Knowledge"

# Index all documents in the directory
for (root,dirs,files) in os.walk(docs_dir):
    # print(len(dirs), len(files))
    for filename in files:
        if filename.endswith(".md"):  # Adjust this for your document types
            filepath = os.path.join(root, filename)
            # print(filepath)
            # print(os.path.exists(filepath))
            index_document(filepath)

print("Indexing complete!")
print("Total Files: ", TOTAL_FILES)
print("No. of file in which Error Occured: ", ERR_FILES)