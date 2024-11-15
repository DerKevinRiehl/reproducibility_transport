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




###############################################################################
############################## METHODS
###############################################################################

def loadArticle(path, file):
    f = open(xml_path+file, "r", encoding="utf-8")
    content = f.read()
    f.close()
    article_nr = file.split("_")[1].split(".")[0]
    return extract_text_from_malformed_xml(content), article_nr
    
def extract_text_from_malformed_xml(xml_string):
    text_content = re.sub(r'<[^>]+>', ' ', xml_string)
    text_content = re.sub(r'\s+', ' ', text_content).strip()
    return text_content

def clean_string_XChars(input_string):
    try:
        decoded = input_string.encode('raw_unicode_escape').decode('utf-8')
    except UnicodeDecodeError:
        decoded = input_string
    cleaned = re.sub(r'[^\x20-\x7E]', ' ', decoded)
    cleaned = ' '.join(cleaned.split())
    return cleaned

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

journal = "journal_2"
journal = "journal_3"
journal = "journal_4"
journal = "journal_5"
journal = "journal_6"
journal = "journal_7"
journal = "journal_8"
journal = "journal_9"
journal = "journal_10"
journal = "journal_11"
journal = "journal_14"
journal = "journal_15"

xml_path = "../data/pipeline/data/"+journal+"/xmls/"
target_path = "../data/pipeline/a_processed_data/"+journal+"_length.txt"

files = os.listdir(xml_path)

f = open(target_path, "w+")

for file in files:
    # retrieve clean article text
    content, article_nr = loadArticle(xml_path, file)
    content = content.replace("\\n", " ")
    content = content.replace("\\r", " ")
    content = content.replace("\n", " ")
    content = content.replace("\r", " ")
    content = content.replace(" . ", " ")
    content = content.replace(" , ", " ")
    content = clean_string_XChars(content)
    content = clean_urls(content)
    parts = content.split(" ")
    # count length
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