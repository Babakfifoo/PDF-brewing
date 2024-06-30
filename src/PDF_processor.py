#%%
from pybtex.database import parse_file
import sys
sys.path.append("../src/")
sys.path.append("../")
import os
import glob
import json
from src import loadPDFS
#%%
        
bib_data = parse_file('../data/raw_pdfs/European Planning Studies/Exported Items.bib')

pdf_dir = "../data/raw_pdfs/European Planning Studies/files/"
json_dir = "../data/texts/"

for entry in bib_data.entries.values():
    fname = entry.fields.get("file").split(":")[0]
    paragraphs = loadPDFS.extract_pdf_text(pdf_dir + fname)
    
    parsed_entry = dict(
        title = entry.fields.get("title"),
        doi = entry.fields.get("doi"),
        year = entry.fields.get("year"),
        keywords = entry.fields.get("keywords"),
        paragraphs = paragraphs
    )
    with open(json_dir + fname.replace(".pdf", ".json"), "w", encoding="utf-8") as output:
        output.write(json.dumps(parsed_entry).encode('utf-8').decode('unicode_escape'))
    
    
# %%

# %%
