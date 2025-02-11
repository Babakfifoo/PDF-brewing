#%%
import sys
sys.path.append("../src/")
sys.path.append("../")
import glob
import fitz
import re
import nltk
#%% 

pdf_fs = glob.glob("../data/raw_pdfs/*.pdf")
#%% 

def fix_block(block):
    block = re.sub("\\xad\\n", "", block)
    block = re.sub("\\n", " ", block)
    return(block)

# %%
pdf_fs = glob.glob("../data/raw_pdfs/*.pdf")
for pdf in pdf_fs:
    doc = fitz.open(pdf)
    pages = [page.get_text("blocks") for page in doc]
    blocks = []
    for i, page in enumerate(pages):
        for block in page[1:-1]:
            block = block[4]
            block = re.sub("Fig.", "figure", block)
            blocks.append(block)

    blocks = list(map(lambda s:nltk.tokenize.sent_tokenize(s), blocks))
    sentences = [item for sublist in blocks for item in sublist]
    sentences = list(map(lambda x: re.sub(r'\s+'," ", x), sentences))
    with open(f"../data/texts/{pdf.split("/")[-1]}.txt", 'w') as output:
        for s in sentences:
            if s.contains(" "):
                next
            if bool(re.match(r"[0-9]+\.",s[0:3] )):
                output.write("\n" + s)
            elif bool(re.match(r'[A-Z]', s[0])):
                output.write("\n" + s)
            else:
                output.write(" " + s)
    print(pdf.split("/")[-1], "  --- DONE.")
# %%

# %%
