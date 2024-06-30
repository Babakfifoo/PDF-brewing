#%%
import sys
sys.path.append("../src/")
sys.path.append("../")
import os
import glob
import fitz
import re
from itertools import chain
import json
# %%


word_correction = {
    "Fig.":"Figure"
}

def is_Cap(s):
    return bool(re.match("^[A-Z]+$", s))

def extract_paragraphs(page):
    paragraphs = []
    for block in page.get_text("blocks"):
        if block[2] - block[0] < 350:
            continue
        paras = block[4].replace("-\n", "").strip()
        paras = re.split(r"[\.\!\?\;]\n", paras, maxsplit=0, flags=0)
        paras = [para.replace("\n", " ") + "."  for para in paras]
        paragraphs.append(paras)
    return(paragraphs)

def extract_pdf_text(doc):
    
    pages = list(map(extract_paragraphs, doc))

    tes = list(chain.from_iterable(pages))
    tes = list(chain.from_iterable(tes))
    paragraphs = []
    for i, para in enumerate(tes[:-1]):
        for k,v in word_correction.items():
            para = para.replace(k,v)
        if not is_Cap(tes[i][0]):
            continue
        if not is_Cap(tes[i+1][0]) :
            paragraphs.append(tes[i] + tes[i+1])
            continue
        paragraphs.append(para)
    return(paragraphs)
# %%
pdf_fs = glob.glob("../data/raw_pdfs/European Planning Studies/files/*.pdf")


for file_path in pdf_fs:
    doc = fitz.open(file_path)
    fname = os.path.basename(file_path).replace(".pdf", ".json")
    paragraphs = extract_pdf_text(doc)
    with open(f"../data/texts/{fname}", "w", encoding="utf-8") as output:
        output.write(json.dumps(paragraphs).encode('utf-8').decode('unicode_escape'))
# %%
