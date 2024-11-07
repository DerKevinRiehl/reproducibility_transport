###############################################################################
### Author: Kevin Riehl <kriehl@ethz.ch>
### Date: 01.11.2024
### Organization: ETH Zürich, Institute for Transport Planning and Systems (IVT)
### Project: Reproducibility of Simulation Studies in Transportation
###############################################################################
### This file goes through all articles and extracts information about the
### articles meta data, and URLs that are linked in the article.
### As a result for files are created:
###    - journal_X_articleInfos.xlsx  (containing information about year, date, title, doi, issue, volume)
###    - journal_X_keywords.xlsx      (containing count information of how often specific keywords occur in the text)
###    - journal_X_urls.xlsx          (containing a list of all URLs that were mentioned in each article)
###    - journal_X_final.xlsx         (containing a combination of all previous files, filtering only relevant URLs related to repositories)
### This file works for journal 13 that was downloaded in PDF and HTML format.
###############################################################################




###############################################################################
############################## Imports
###############################################################################
import os
import pandas as pd
from urllib.parse import urlparse
import PyPDF2
import re
from datetime import datetime




###############################################################################
############################## Program Settings & Parameters
###############################################################################
main_path = "./data/"
journal = "journal_13"




###############################################################################
############################## Methods
###############################################################################
def determineDownloadTypes(journal_path):
    folders = os.listdir(journal_path)
    folders = [f for f in folders if f!="article_links.txt" ]
    return folders

def extractPdfContent(pdf_path):
    full_text = ""
    urls = set()
    try:
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page in pdf_reader.pages:
                # Extract text
                full_text += page.extract_text()
                # Extract URLs from text
                text_urls = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', full_text)
                urls.update(text_urls)
                # Extract hyperlinks
                if '/Annots' in page:
                    for annot in page['/Annots']:
                        obj = annot.get_object()
                        if obj.get('/Subtype') == '/Link' and '/A' in obj:
                            if '/URI' in obj['/A']:
                                urls.add(str(obj['/A']['/URI']))
        return full_text, list(urls)
    except:
        return "", []

def findKeyInText(text, key):
    indexes = []
    start = -1
    while True:
        result = text.find(key, start+1)
        if result==-1:
            break
        else:
            indexes.append(result)
            start = result
    return indexes

def extractURLsFromXML(text):
    indexes = findKeyInText(text, "http")
    indexes2 = findKeyInText(text, "www")
    indexes = list(set(indexes).union(set(indexes2)))
    list_urls = []
    urls_to_add = []
    # find urls
    for idx in indexes:
        url = text[idx:]
        url = url.split("</")[0]
        if "\"" in url:
            url = url.split("\"")[0]
        if "</" in url:
            url = url.split("</")[0]
        if " " in url:
            parts = url.split(" ")
            for p in parts:
                urls_to_add.append(p)
        else:
            urls_to_add.append(url)
    # filter urls
    for u in urls_to_add:
        if len(u)<5:
            continue
        if not "/" in u:
            continue
        if "," in u or "(" in u or ")" in u:
            continue
        if u.endswith("."):
            u = u[:-1]
        if u.endswith("\n"):
            u = u[:-1]
        if u.endswith("\\n"):
            u = u[:-2]
        if u.endswith("."):
            u = u[:-1]
        list_urls.append(u)
    return list(set(list_urls))
    
def extractDomains(urls):
    domains = []
    for url in urls:
        parsed_url = urlparse(url)
        domain = parsed_url.netloc
        if domain.startswith('www.'):
            domain = domain[4:]
        if domain not in domains:
            if domain!="":
                domains.append(domain)
    return domains

def extractYear(date_string):
    match = re.search(r'\d{4}', date_string)
    return match.group() if match else None

def convertDateFormat(date_string):
    # Parse the input string
    date_object = datetime.strptime(date_string, '%d%B%Y')
    
    # Format the date object to the desired output format
    return date_object.strftime('%Y-%m-%d')




###############################################################################
############################## Main Code
###############################################################################

download_types = determineDownloadTypes(main_path+journal)
article_index_df = pd.read_csv("./data/Journal_13.txt")
article_index_df['url'] = 'https://doi.org/' + article_index_df['url']
article_index_df["article_nr"] = range(1, len(article_index_df) + 1)

list_article_urls = []
list_article_words = []
list_article_infos = []
for idx, row in article_index_df.iterrows():
    if int(row["article_nr"])<1301:
        continue
    print("Reading article from", journal," article_nr:", row["article_nr"])    
    # Process Articles to get lists of URLS
    content, list_urls = extractPdfContent(main_path+journal+"/article_"+str(row["article_nr"])+".pdf")

    print("\tURLS found:", len(list_urls))
    for url in list_urls:
        list_article_urls.append([journal, row["article_nr"], url])
    # Process Articles to get word counts
    list_article_words.append([journal, row["article_nr"], 
                               content.lower().count("repositor"),
                               content.lower().count("data"),
                               content.lower().count("simulat")
                               ])
    
    # Article infos
    if len(content)==0:
        doi = ""
        date = ""
        title = ""
        volume = ""
        issue = ""
        year = ""
        date2 = ""
    else:
        if "DOI:" not in content:
            doi = ""
            title = "???"
        else:
            doi = content.split("DOI:")[1].split("\n")[0]
            title = " ".join(content.split("DOI:")[1].split("Correspondence")[0].split("\n")[1:-1])
        if not "Accepted:" in content:
            date =""
            year =""
            date2=""
        else:
            date = content.split("Accepted:")[1].split("\n")[0]
            year = extractYear(date)
            date2 = convertDateFormat(date)
        volume = "?"
        issue = "?"  
        
    list_article_infos.append([journal, row["article_nr"],
                               year,
                               doi.strip(),
                               date2,
                               title.strip(),
                               volume.strip(),
                               issue.strip()])

df_urls = pd.DataFrame(list_article_urls, columns=["journal", "article_nr", "url"])
df_keywords = pd.DataFrame(list_article_words, columns=["journal", "article_nr", "repository", "data", "simulation"])
df_article_infos = pd.DataFrame(list_article_infos, columns=["journal", "article_nr", "year", "doi", "date", "title", "volume", "issue"])
df_article_infos['title'] = df_article_infos['title'].str.slice(0, 200)
df_urls.to_excel("processed_data/"+journal+"_urls.xlsx")
df_keywords.to_excel("processed_data/"+journal+"_keywords.xlsx")
df_article_infos.to_excel("processed_data/"+journal+"_articleInfos.xlsx")

relevant_url = []
for idx, row in df_urls.iterrows():
    url = row["url"].lower()
    if "github" in url or "drive.google" in url or "bitbucket" in url or "sourceforge" in url or "mendeley" in url or 'docs.google.com/' in url or "youtube" in url or "zenodo" in url:
        relevant_url.append(True)
    else:
        relevant_url.append(False)
df_filtered = df_urls.copy()
df_filtered["rel"] = relevant_url
df_filtered = df_filtered[df_filtered["rel"]==True]
del df_filtered["rel"]
df_filtered = df_filtered.merge(df_keywords, on=["journal", "article_nr"], how="left")
df_filtered = df_filtered.merge(df_article_infos, on=["journal", "article_nr"], how="left")
df_filtered.to_excel("processed_data/"+journal+"_final.xlsx")
