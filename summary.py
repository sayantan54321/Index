import os
import json
import glob
from transformers import pipeline

def generate_summaries(directory_path):
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")    
    summaries_dict = {}    
    txt_files = glob.glob(os.path.join(directory_path, '**', '*.txt'), recursive=True)    
    if not os.path.isdir(directory_path):
        raise ValueError(f"The specified path is not a directory: {directory_path}")
    if not txt_files:
        raise ValueError(f"No markdown files found in {directory_path}")    
    for file_path in txt_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()            
            max_length = 1024
            truncated_content = content[:max_length*4]            
            summary = summarizer(truncated_content, 
                                 max_length=300, 
                                 min_length=100, 
                                 do_sample=False)[0]['summary_text']            
            full_summary = f"Here is a detailed summary of the text:\n\n{summary}"            
            full_path = os.path.relpath(file_path, directory_path)
            summaries_dict[full_path] = full_summary
            print(f"Processed: {full_path}")
        except Exception as e:
            print(f"Error processing {file_path}: {e}")
    return summaries_dict
directory_path = '/root/PERPLEXICA/Index/ramayana_cleaned'
output_file = os.path.join(directory_path, 'markdown_summaries_ramayana.json')
summaries = generate_summaries(directory_path)
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(summaries, f, indent=2)
print(f"Summaries saved to {output_file}")
print("\nFirst few summaries:")
for key, value in list(summaries.items())[:3]:
    print(f"{key}:\n{value[:300]}...\n")
print(f"\nTotal files processed: {len(summaries)}")