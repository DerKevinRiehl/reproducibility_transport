###############################################################################
### Author: Kevin Riehl <kriehl@ethz.ch>
### Date: 01.11.2024
### Organization: ETH Zürich, Institute for Transport Planning and Systems (IVT)
### Project: Reproducibility of Simulation Studies in Transportation
###############################################################################
### This file merges tables from previous steps, cleans data, renames columns,
### in order to derive a final, presentable dataset for publication and analysis.
### One output îs created: 
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
df_citations = pd.read_csv("../data/pipeline/b_merged_data/Article_Citations_Crossref.csv")
df_article_infos = pd.read_excel("../data/pipeline/b_merged_data/ArticleInfos_manual.xlsx")
df_article_urls = pd.read_excel("../data/pipeline/b_merged_data/ArticleURLs_manual_2.xlsx")
df_article_repos = pd.read_excel("../data/pipeline/b_merged_data/Repository_Review_manual_2.xlsx")
df_article_length = pd.read_csv("../data/pipeline/b_merged_data/Article_Lengths.csv")

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

# Merge Lengths with Article Infos
df_article_infos = df_article_infos.merge(df_article_length, on=["journal", "article_nr"], how="left")

# Determine Relevant URLs
df_article_urls_rel = df_article_urls[df_article_urls["valid_url"]=="yes"]
print(len(df_article_urls_rel))
df_article_urls_rel = df_article_urls_rel[df_article_urls_rel["own_url"]=="yes"]
print(len(df_article_urls_rel))

# Include has_repository Information in Article Infos
df_article_urls_rel['key'] = df_article_urls_rel['journal'] + '_' + df_article_urls_rel['article_nr'].astype(str)
df_article_repos['key'] = df_article_repos['journal'] + '_' + df_article_repos['article_nr'].astype(str)
df_article_infos['key'] = df_article_infos['journal'] + '_' + df_article_infos['article_nr'].astype(str)
infos_keys = set(df_article_urls_rel['key'])
df_article_infos['has_repository'] = df_article_infos['key'].isin(infos_keys)
infos_keys = set(df_article_repos["key"])
df_article_infos['has_valid_repository'] = df_article_infos['key'].isin(infos_keys)

# Prepare Summary Rating Of Article Repos for Merging
df_article_repos_agg = df_article_repos[['journal', 'article_nr', 'repo_type', 
                                         'video', 'code', 'dataset', 'model', 
                                         'documentation', 'license', 'score 1..5']]
    # dummy for each repo type
repo_types = ["GitHub", "GoogleDrive", "YouTube", "Zenodo", "BitBucket", "DropBox", "Mendeley", "SourceForge", "GoogleDocs"]
for r_type in repo_types:
    df_article_repos_agg['has_'+r_type] = df_article_repos_agg['repo_type'].str.contains(r_type, case=False)
    github_mask = df_article_repos_agg.groupby(['journal', 'article_nr'])['has_'+r_type].transform('any')
    df_article_repos_agg['dummy_'+r_type] = github_mask
    df_article_repos_agg.drop('has_'+r_type, axis=1, inplace=True)
    # other article features
df_article_repos_agg['video'] = df_article_repos_agg['video'].str.lower()
video_mask = df_article_repos_agg.groupby(['journal', 'article_nr'])['video'].transform(lambda x: (x == 'yes').any())
df_article_repos_agg['has_video'] = video_mask
df_article_repos_agg['code'] = df_article_repos_agg['code'].str.lower()
code_mask = df_article_repos_agg.groupby(['journal', 'article_nr'])['code'].transform(lambda x: (x != 'no').any())
df_article_repos_agg['has_code'] = code_mask
df_article_repos_agg['dataset'] = df_article_repos_agg['dataset'].str.lower()
dataset_mask = df_article_repos_agg.groupby(['journal', 'article_nr'])['dataset'].transform(lambda x: (x == 'yes').any())
df_article_repos_agg['has_dataset'] = dataset_mask
df_article_repos_agg['model'] = df_article_repos_agg['model'].str.lower()
model_mask = df_article_repos_agg.groupby(['journal', 'article_nr'])['model'].transform(lambda x: (x == 'yes').any())
df_article_repos_agg['has_model'] = model_mask
df_article_repos_agg['documentation'] = df_article_repos_agg['documentation'].str.lower()
documentation_mask = df_article_repos_agg.groupby(['journal', 'article_nr'])['documentation'].transform(lambda x: (x == 'yes').any())
df_article_repos_agg['has_documentation'] = documentation_mask
df_article_repos_agg['license'] = df_article_repos_agg['license'].str.lower()
license_mask = df_article_repos_agg.groupby(['journal', 'article_nr'])['license'].transform(lambda x: (x != 'none').any())
df_article_repos_agg['has_license'] = license_mask
df_article_repos_agg['score 1..5'] = pd.to_numeric(df_article_repos_agg['score 1..5'], errors='coerce')
df_article_repos_agg['repo_score'] = df_article_repos_agg.groupby(['journal', 'article_nr'])['score 1..5'].transform('max')

df_article_repos_agg = df_article_repos_agg[["journal", "article_nr",
                                             'dummy_GitHub', 'dummy_GoogleDrive', 
                                             'dummy_YouTube', 'dummy_Zenodo', 
                                             'dummy_BitBucket', 'dummy_DropBox', 
                                             'dummy_Mendeley', 'dummy_SourceForge',
                                             'dummy_GoogleDocs', 'has_video', 
                                             'has_code', 'has_dataset', 'has_model',
                                             'has_documentation', 'has_license', 
                                             'repo_score']]
df_article_repos_agg = df_article_repos_agg.drop_duplicates()

# Include Repository Information into Article information
df_article_infos = df_article_infos.merge(df_article_repos_agg, on=["journal", "article_nr"], how="left")

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
                                      "n_chars", "n_words",
                                      "has_repository", "has_valid_repository",
                                      'repository', 'data', 'simulation',
                                      "date", "title",
                                      "num_cits_per_year", "num_log_cits", "num_log_cits_per_year",
                                      
                                      'dummy_GitHub', 'dummy_GoogleDrive',
                                      'dummy_YouTube', 'dummy_Zenodo', 
                                      'dummy_BitBucket', 'dummy_DropBox',
                                      'dummy_Mendeley', 'dummy_SourceForge', 
                                      'dummy_GoogleDocs', 'has_video',
                                      'has_code', 'has_dataset', 'has_model', 
                                      'has_documentation', 'has_license', 'repo_score'
                                      ]]
df_article_infos = df_article_infos.rename(columns={
    "doi_clean": "doi", 
    "clean_year": "article_year", 
    "date":"date_online", 
    "repository": "wc_repository", 
    "data": "wc_data", 
    "simulation":"wc_simulation", 
    "title":"article_title",
    "n_chars": "num_chars",
    "n_words": "num_words",
    })




###############################################################################
############################## Save Final ArticleInfos
###############################################################################
df_article_infos.to_excel("../data/pipeline/c_clean_data/ArticleInfos.xlsx", index=False)