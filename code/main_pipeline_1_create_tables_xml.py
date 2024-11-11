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
### This file works for all journals what were downloaded in XML format.
### Journals: 3,4,5,6,7,8,9,10,11,14,15
###############################################################################




###############################################################################
############################## Imports
###############################################################################
import os
import numpy as np
import pandas as pd
from urllib.parse import urlparse




###############################################################################
############################## Program Settings & Parameters
###############################################################################
main_path = "data/pipeline/data/"
journal = "journal_2"
# journal = "journal_3"
# journal = "journal_4"
# journal = "journal_5"
# journal = "journal_6"
# journal = "journal_7"
# journal = "journal_8"
# journal = "journal_9"
# journal = "journal_10"
# journal = "journal_11"
# journal = "journal_14"
# journal = "journal_15"




###############################################################################
############################## Methods
###############################################################################
def determineDownloadTypes(journal_path):
    folders = os.listdir(journal_path)
    folders = [f for f in folders if f!="article_links.txt" ]
    return folders

def loadArticlesIndex(journal_path):
    df = pd.read_csv(journal_path+"article_links.txt")
    df["article_nr"] = np.arange(1, len(df) + 1)
    return df

def loadArticleContent_XML(journal_path, article_nr):
    f = open(journal_path+"xmls/article_"+str(article_nr)+".txt", "r", encoding="utf-8")
    content = f.read()
    f.close()
    return content

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




###############################################################################
############################## Main Code
###############################################################################

download_types = determineDownloadTypes(main_path+journal)
article_index_df = loadArticlesIndex(main_path+journal+"/")

list_article_urls = []
list_article_words = []
list_article_infos = []
for idx, row in article_index_df.iterrows():
    if int(row["article_nr"]<685):
        continue
    print("Reading article from", journal," article_nr:", row["article_nr"])    
    # Process Articles to get lists of URLS
    content = loadArticleContent_XML(main_path+journal+"/", row["article_nr"])
    list_urls = extractURLsFromXML(content)
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
    if "<dc:identifier>" in content:
        doi = content.split("<dc:identifier>")[1].split("</")[0]
    else:
        doi = ""
    if "<prism:coverDate>" in content:        
        date = content.split("<prism:coverDate>")[1].split("</")[0]
    else:
        date = ""
    if "<dc:title>" in content:
        title = content.split("<dc:title>")[1].split("</")[0]
    else:
        title = "[UNKNOWN]"
    if "<prism:volume>" in content:
        volume = content.split("<prism:volume>")[1].split("</")[0]
    else:
        volume = ""
    if "<prism:issueIdentifier>" in content:
        issue = content.split("<prism:issueIdentifier>")[1].split("</")[0]
    else:
        issue = ""
    list_article_infos.append([journal, row["article_nr"],
                               date.split("-")[0].strip(),
                               doi.strip(),
                               date.strip(),
                               title.strip(),
                               volume.strip(),
                               issue.strip()])
df_urls = pd.DataFrame(list_article_urls, columns=["journal", "article_nr", "url"])
df_keywords = pd.DataFrame(list_article_words, columns=["journal", "article_nr", "repository", "data", "simulation"])
df_article_infos = pd.DataFrame(list_article_infos, columns=["journal", "article_nr", "year", "doi", "date", "title", "volume", "issue"])
df_urls.to_csv("data/pipeline/a_processed_data/"+journal+"_urls.csv")
df_keywords.to_excel("data/pipeline/a_processed_data/"+journal+"_keywords.xlsx")
df_article_infos.to_excel("data/pipeline/a_processed_data/"+journal+"_articleInfos.xlsx")

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
df_filtered.to_excel("data/pipeline/a_processed_data/"+journal+"_final.xlsx")
