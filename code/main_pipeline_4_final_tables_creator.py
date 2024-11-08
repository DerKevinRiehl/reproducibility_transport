###############################################################################
### Author: Kevin Riehl <kriehl@ethz.ch>
### Date: 01.11.2024
### Organization: ETH Zürich, Institute for Transport Planning and Systems (IVT)
### Project: Reproducibility of Simulation Studies in Transportation
###############################################################################
### This file merges tables from previous steps, cleans data, renames columns,
### in order to derive a final, presentable dataset for publication and analysis.
### Two outputs are created: 
###    - ArticleInfos.xlsx
###############################################################################




###############################################################################
############################## Imports
###############################################################################
import pandas as pd
import numpy as np




###############################################################################
############################## Merge ArticleInfos
###############################################################################

# Load Source Tables
df_citations = pd.read_csv("b_merged_data/Article_Citations_Crossref.csv")
df_article_infos = pd.read_excel("b_merged_data/ArticleInfos_manual.xlsx")
df_article_urls = pd.read_excel("b_merged_data/ArticleURLs_manual_2.xlsx")

# Remove unncessary columns
del df_citations['Unnamed: 0']
del df_article_infos['Unnamed: 0']
del df_article_urls['Unnamed: 0']
del df_article_urls['Unnamed: 0.1']

# Merge Citations with Article Infos
df_article_infos = df_article_infos.merge(df_citations, on=["journal", "article_nr"], how="left")
def clean_year(row):
    if pd.notna(row['num_yearp']) and row['num_yearp'] != -1:
        return row['num_yearp']
    else:
        return row['year']

# Determine Relevant URLs
df_article_urls_rel = df_article_urls[df_article_urls["valid_url"]=="yes"]
print(len(df_article_urls_rel))
df_article_urls_rel = df_article_urls_rel[df_article_urls_rel["own_url"]=="yes"]
print(len(df_article_urls_rel))
df_article_urls_rel = df_article_urls_rel[df_article_urls_rel["available_url"]=="yes"]
print(len(df_article_urls_rel))

# Include has_repository Information in Article Infos
df_article_urls_rel['key'] = df_article_urls_rel['journal'] + '_' + df_article_urls_rel['article_nr'].astype(str)
df_article_infos['key'] = df_article_infos['journal'] + '_' + df_article_infos['article_nr'].astype(str)
infos_keys = set(df_article_urls_rel['key'])
df_article_infos['has_repository'] = df_article_infos['key'].isin(infos_keys)

# Clean Year Field, Calculate Citation Metrics    
df_article_infos['clean_year'] = df_article_infos.apply(clean_year, axis=1)
df_article_infos['clean_year_since_publication'] = 2024-df_article_infos['clean_year']+1
df_article_infos["num_cits_per_year"] = df_article_infos["num_cits"] / df_article_infos['clean_year_since_publication']
df_article_infos["num_log_cits"] = np.log(df_article_infos["num_cits"])
df_article_infos['num_log_cits'] = df_article_infos['num_log_cits'].replace([np.inf, -np.inf], np.nan)
df_article_infos["num_log_cits_per_year"] = df_article_infos["num_log_cits"] / df_article_infos['clean_year_since_publication']
df_article_infos.loc[(df_article_infos['num_cits'].isna()) | (df_article_infos['num_cits'] == -1), 'num_cits_per_year'] = np.nan
df_article_infos.loc[(df_article_infos['num_cits'].isna()) | (df_article_infos['num_cits'] == -1), 'num_log_cits'] = np.nan
df_article_infos.loc[(df_article_infos['num_cits'].isna()) | (df_article_infos['num_cits'] == -1), 'num_log_cits_per_year'] = np.nan

# Clean Columns
df_article_infos = df_article_infos[["journal", "article_nr", "clean_year", 
                                      "doi_clean", "volume", "issue", 
                                      "num_auths", "num_refs", "num_cits", 
                                      "has_repository",
                                      'repository', 'data', 'simulation',
                                      "date", "title",
                                      "num_cits_per_year", "num_log_cits", "num_log_cits_per_year"]]
df_article_infos = df_article_infos.rename(columns={
    "doi_clean": "doi", 
    "clean_year": "article_year", 
    "date":"date_online", 
    "repository": "wc_repository", 
    "data": "wc_data", 
    "simulation":"wc_simulation", 
    "title":"article_title"
    })
