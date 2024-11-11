###############################################################################
### Author: Kevin Riehl <kriehl@ethz.ch>
### Date: 01.11.2024
### Organization: ETH Zürich, Institute for Transport Planning and Systems (IVT)
### Project: Reproducibility of Simulation Studies in Transportation
###############################################################################
### This file calls the Cross Ref API "https://api.crossref.org/works/"+doi, to
### derive information about the citation counts for each article.
### Two outputs are created: 
###    - Article_Citations_Crossref.csv  (containing an overview of all downloaded articles and citation data)
###############################################################################




###############################################################################
############################## Imports
###############################################################################
import pandas as pd
import requests
import json




###############################################################################
############################## Methods
###############################################################################

def getInformationFromResponse(data):
    num_refs = -1
    num_cits = -1
    num_auths = -1
    num_yearp = -1
    try:
        # number of references    
        num_refs = data["message"]["reference-count"]
        # number of citations
        num_cits = data["message"]["is-referenced-by-count"]
        # number of authors
        num_auths = len(data["message"]["author"])
        # year published
        num_yearp = data["message"]["published"]["date-parts"][0][0]
    except:
        pass
    return num_refs, num_cits, num_auths, num_yearp

def getInformationFromCrossRefAPI(doi):
    url = "https://api.crossref.org/works/"+doi
    data = None
    # Send GET request to the API
    response = requests.get(url)
    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()
        # Pretty print the JSON data
        # print(json.dumps(data, indent=2))
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
    num_refs, num_cits, num_auths, num_yearp = getInformationFromResponse(data)
    return num_refs, num_cits, num_auths, num_yearp

# doi = "10.1016/j.bioactmat.2020.11.006"
# print(getInformationFromCrossRefAPI(doi))


df = pd.read_excel("data/pipeline/b_merged_data/ArticleInfos_manual.xlsx")
def clean_doi_string(doi):
    try:
        doi_clean = doi.strip()
        if doi_clean.startswith("doi:"):
            doi_clean = doi_clean[4:]
        if doi_clean.startswith("https://www.tandfonline.com/doi/full/"):
            doi_clean = doi_clean.split("https://www.tandfonline.com/doi/full/")[1]
        if doi_clean.startswith("https://doi.org/"):
            doi_clean = doi_clean.split("https://doi.org/")[1]
        return doi_clean
    except:
        return doi
df['doi_clean'] = df['doi'].apply(clean_doi_string)

def retrieveInfo(row):
    print(row["journal"], row["article_nr"])
    num_refs, num_cits, num_auths, num_yearp = getInformationFromCrossRefAPI(row["doi_clean"])
    print("\t", num_refs, num_cits, num_auths, num_yearp)
    return num_refs, num_cits, num_auths, num_yearp
lst_data = []
ctr = 0
for idx, row in df.iterrows():
    ctr+=1
    print(">>",ctr, idx, len(df))
    num_refs, num_cits, num_auths, num_yearp = retrieveInfo(row)
    lst_data.append([num_refs, num_cits, num_auths, num_yearp, row["doi_clean"], row["journal"], row["article_nr"]])
    # df[["cra_refs", "cra_cits", "cra_auths", "cra_yearp"]] = df.apply(retrieveInfo, axis=1, result_type="expand")

dfX = pd.DataFrame(lst_data, columns=["num_refs", "num_cits", "num_auths", "num_yearp", "doi_clean", "journal", "article_nr"])
dfX.to_csv("data/pipeline/b_merged_datA/Article_Citations_Crossref.csv")