###############################################################################
### Author: Kevin Riehl <kriehl@ethz.ch>
### Date: 01.11.2024
### Organization: ETH Zürich, Institute for Transport Planning and Systems (IVT)
### Project: Reproducibility of Simulation Studies in Transportation
###############################################################################
### This file counts the number of words and characters in an article.
###############################################################################




###############################################################################
############################## IMPORTS
###############################################################################
import re
import os
from pypdf import PdfReader




###############################################################################
############################## METHODS
###############################################################################

def loadArticle(path, file):
    try:
        reader = PdfReader(path+file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
    except:
        text = ""
    article_nr = file.split("_")[1].split(".")[0]
    return text, article_nr

def clean_urls(content):
    parts = content.split(" ")
    complete = ""
    for part in parts:
        if part=="b'":
            continue
        if part.startswith("doi:"):
            continue
        if part.startswith("https://") or part.startswith("http://"):
            continue
        if len(part)<2:
            continue
        if len(part)<5 and (part.startswith("&") or part.startswith("#")):
            continue
        complete+=part.strip()+" "
    return complete




###############################################################################
############################## MAIN CODE
###############################################################################

journal = "journal_17"

xml_path = "../data/pipeline/data/"+journal+"/pdfs/"
target_path = "../data/pipeline/a_processed_data/"+journal+"_length.txt"

files = os.listdir(xml_path)

f = open(target_path, "w+")

for file in files:
    # retrieve clean article text
    content, article_nr = loadArticle(xml_path, file)
    if content=="":
        length_chars = -1
        length_words = -1
    else:
        content = content.replace("\\n", " ")
        content = content.replace("\\r", " ")
        content = content.replace("\n", " ")
        content = content.replace("\r", " ")
        content = content.replace(" . ", " ")
        content = content.replace(" , ", " ")
        content = clean_urls(content)
        parts = content.split(" ")
        length_chars = len(content)
        length_words = len(parts)
    # write result
    f.write(journal)
    f.write("\t")
    f.write(article_nr)
    f.write("\t")
    f.write(str(length_chars))
    f.write("\t")
    f.write(str(length_words))
    f.write("\n")
    print(journal, article_nr, length_chars, length_words)
f.close()