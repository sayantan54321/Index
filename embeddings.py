import os
import json
from sentence_transformers import SentenceTransformer
import glob

def generate_embeddings(directory_path):
    model = SentenceTransformer('all-mpnet-base-v2')    
    embeddings_dict = {}    
    txt_files = glob.glob(os.path.join(directory_path, '**', '*.txt'), recursive=True)    
    if not os.path.isdir(directory_path):
        raise ValueError(f"The specified path is not a directory: {directory_path}")
    
    if not txt_files:
        raise ValueError(f"No markdown files found in {directory_path}")    
    for file_path in txt_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()            
            embedding = model.encode(content).tolist()            
            # full_path = os.path.relpath(file_path, directory_path)
            embeddings_dict[file_path] = embedding
            print(f"Processed: {file_path}")
        except Exception as e:
            print(f"Error processing {file_path}: {e}")
    
    return embeddings_dict
directory_path = '/root/PERPLEXICA/Index/ramayana_cleaned'
output_file = os.path.join(directory_path, 'markdown_embeddings_ramayana.json')
embeddings = generate_embeddings(directory_path)
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(embeddings, f, indent=2)
print(f"Embeddings saved to {output_file}")
print("\nFirst few embeddings:")
for key, value in list(embeddings.items())[:3]:
    print(f"{key}: {value[:5]}... (truncated)")
print(f"\nTotal files processed: {len(embeddings)}")