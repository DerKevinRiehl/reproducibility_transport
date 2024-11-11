###############################################################################
### Author: Kevin Riehl <kriehl@ethz.ch>
### Date: 01.11.2024
### Organization: ETH Zürich, Institute for Transport Planning and Systems (IVT)
### Project: Reproducibility of Simulation Studies in Transportation
###############################################################################
### This file analyses the merged information tables, produces tables and figures.
###############################################################################




###############################################################################
############################## Imports
###############################################################################
import pandas as pd
import matplotlib.pyplot as plt




###############################################################################
############################## Constants
###############################################################################
simulation_threshold = 5

df_articleinfos = pd.read_excel("../data/ArticleInformation/ArticleInfos.xlsx")
year_col = "article_year"
simu_col = 'wc_simulation'

df_articleinfos_valid = df_articleinfos.copy()
df_articleinfos_valid = df_articleinfos_valid[df_articleinfos_valid[year_col].notna()]

journals = ["journal_2", "journal_3", "journal_4", "journal_5", "journal_6", 
            "journal_7", "journal_8", "journal_9", "journal_10", "journal_11", 
            "journal_13", "journal_14", "journal_15", "journal_17", "journal_18"]

journal_names = {
    "journal_2": "Transportation Research \n Part C",
    "journal_3": "Transportation Research \n Part D",
    "journal_4": "Transportation Research \n Part A",
    "journal_5": "Transportation Research \n Part E",
    "journal_6": "Transportation Research \n Part E",
    "journal_7": "Transport Policy",
    "journal_8": "Transportation Research \n Part B",
    "journal_9": "Journal of \n Transport Geography",
    "journal_10": "Transportation Research \n Part F",
    "journal_11": "Transportation Research \n Interdisciplinary Perspectives",
    "journal_13": "Computer‐Aided Civil and \n Infrastructure Engineering",
    "journal_14": "Journal of Air \n Transport Management",
    "journal_15": "Transportation \n Research Procedia",
    "journal_17": "Transport Reviews",
    "journal_18": "International Journal \n of Pavement Engineering"
}


all_years = pd.DataFrame({year_col: range(2000, 2024)})




###############################################################################
############################## Analysis 1: Table Number Articles And Simulations Per Journal
###############################################################################

df_articles_per_journal = df_articleinfos_valid.groupby('journal').size().reset_index(name='count')
df_simulation_studies_per_journal = df_articleinfos_valid[df_articleinfos_valid[simu_col] >= simulation_threshold].groupby("journal").size().reset_index(name="count")

mask = (df_articleinfos_valid[simu_col] >= simulation_threshold) & (df_articleinfos_valid["has_valid_repository"] == True)
df_vrepo_studies_per_journal = df_articleinfos_valid[mask].groupby("journal").size().reset_index(name="count")

df_articles_journal_summary = df_articles_per_journal.copy()
df_articles_journal_summary = df_articles_journal_summary.merge(df_simulation_studies_per_journal, on="journal", how="left")
df_articles_journal_summary = df_articles_journal_summary.merge(df_vrepo_studies_per_journal, on="journal", how="left")
df_articles_journal_summary["ratio"] = df_articles_journal_summary["count_y"]/df_articles_journal_summary["count_x"]*100
df_articles_journal_summary["ratio2"] = df_articles_journal_summary["count"]/df_articles_journal_summary["count_y"]*100
df_articles_journal_summary = df_articles_journal_summary[["journal", "count_y", "count_x", "count", "ratio", "ratio2"]]
df_articles_journal_summary = df_articles_journal_summary.rename(columns=
                                                                 {"count_y": "n_simstud", 
                                                                  "count_x": "n_articles", 
                                                                  "count": "n_withrepo",
                                                                  "ratio": "sh_simstud",
                                                                  "ratio2": "sh_withrepo"
                                                                  })
print("Overall (2000 - 2024)")
print(df_articles_journal_summary)


df_articleinfos_valid_l5y = df_articleinfos_valid[df_articleinfos_valid[year_col]>=2019]
df_articles_per_journal = df_articleinfos_valid_l5y.groupby('journal').size().reset_index(name='count')
df_simulation_studies_per_journal = df_articleinfos_valid_l5y[df_articleinfos_valid_l5y[simu_col] >= simulation_threshold].groupby("journal").size().reset_index(name="count")

mask = (df_articleinfos_valid_l5y[simu_col] >= simulation_threshold) & (df_articleinfos_valid_l5y["has_valid_repository"] == True)
df_vrepo_studies_per_journal = df_articleinfos_valid_l5y[mask].groupby("journal").size().reset_index(name="count")

df_articles_journal_summary = df_articles_per_journal.copy()
df_articles_journal_summary = df_articles_journal_summary.merge(df_simulation_studies_per_journal, on="journal", how="left")
df_articles_journal_summary = df_articles_journal_summary.merge(df_vrepo_studies_per_journal, on="journal", how="left")
df_articles_journal_summary["ratio"] = df_articles_journal_summary["count_y"]/df_articles_journal_summary["count_x"]*100
df_articles_journal_summary["ratio2"] = df_articles_journal_summary["count"]/df_articles_journal_summary["count_y"]*100
df_articles_journal_summary = df_articles_journal_summary[["journal", "count_y", "count_x", "count", "ratio", "ratio2"]]
df_articles_journal_summary = df_articles_journal_summary.rename(columns=
                                                                 {"count_y": "n_simstud", 
                                                                  "count_x": "n_articles", 
                                                                  "count": "n_withrepo",
                                                                  "ratio": "sh_simstud",
                                                                  "ratio2": "sh_withrepo"
                                                                  })
print("Last Five Years (2019 - 2024)")
print(df_articles_journal_summary)




###############################################################################
############################## Analysis 2: Number of Articles & Simulation Studies
###############################################################################

df_articles_per_year = df_articleinfos_valid.groupby(year_col).size().reset_index(name='count')
df_articles_per_year = all_years.merge(df_articles_per_year, on=year_col, how='left')
df_articles_per_year['count'] = df_articles_per_year['count'].fillna(0).astype(int)

df_simulation_studies_per_year = df_articleinfos_valid[df_articleinfos_valid[simu_col] >= simulation_threshold].groupby(year_col).size().reset_index(name="count")
df_simulation_studies_per_year = all_years.merge(df_simulation_studies_per_year, on=year_col, how='left')
df_simulation_studies_per_year['count'] = df_simulation_studies_per_year['count'].fillna(0).astype(int)

mask = (df_articleinfos_valid[simu_col] >= simulation_threshold) & (df_articleinfos_valid["has_repository"] == True)
df_filtered = df_articleinfos_valid[mask]
df_repo_studies_per_year = df_filtered.groupby(year_col).size().reset_index(name="count")
df_repo_studies_per_year = all_years.merge(df_repo_studies_per_year, on=year_col, how='left')
df_repo_studies_per_year['count'] = df_repo_studies_per_year['count'].fillna(0).astype(int)

mask = (df_articleinfos_valid[simu_col] >= simulation_threshold) & (df_articleinfos_valid["has_valid_repository"] == True)
df_filtered = df_articleinfos_valid[mask]
df_vrepo_studies_per_year = df_filtered.groupby(year_col).size().reset_index(name="count")
df_vrepo_studies_per_year = all_years.merge(df_vrepo_studies_per_year, on=year_col, how='left')
df_vrepo_studies_per_year['count'] = df_vrepo_studies_per_year['count'].fillna(0).astype(int)

plt.figure(figsize=(10,3))

plt.subplot(1,3,1)
plt.title("Number of Studies")
plt.plot(df_articles_per_year[year_col], df_articles_per_year["count"], label="All Studies", color="black")
plt.plot(df_simulation_studies_per_year[year_col], df_simulation_studies_per_year["count"], label="Simulation Studies", color="gray")
plt.plot(df_vrepo_studies_per_year[year_col], df_vrepo_studies_per_year["count"], ":", label="with repository", color="gray")
plt.xlabel("Years")
plt.ylabel("Number of Articles")
plt.legend()

plt.subplot(1,3,2)
plt.title("Share of Simulation Studies")
plt.plot(df_simulation_studies_per_year[year_col], df_simulation_studies_per_year["count"]/df_articles_per_year["count"]*100, color="black")
plt.xlabel("Years")
plt.ylabel("Share of All Articles [%]")

plt.subplot(1,3,3)
plt.title("(with Repository)\nShare of Simulation Studies")
plt.plot(df_simulation_studies_per_year[year_col], df_vrepo_studies_per_year["count"]/df_simulation_studies_per_year["count"]*100, color="black")
plt.xlabel("Years")
plt.ylabel("Share of Simulation Articles [%]")

plt.tight_layout()




###############################################################################
############################## Analysis 3: Number of Articles & Simulation Studies Per Journal
###############################################################################


########### Share of Simulation Studies
plt.figure(figsize=(10,5))

ctr = 0
for journal in journals:
    ctr+=1
    plt.subplot(3,5,ctr)
    plt.title(journal_names[journal]+"\n("+journal+")", fontsize=9)
    
    df_journal = df_articleinfos_valid[df_articleinfos_valid["journal"]==journal]
    
    df_articles_per_year = df_journal.groupby(year_col).size().reset_index(name='count')
    df_articles_per_year = all_years.merge(df_articles_per_year, on=year_col, how='left')
    df_articles_per_year['count'] = df_articles_per_year['count'].fillna(0).astype(int)

    df_simulation_studies_per_year = df_journal[df_journal[simu_col] >= simulation_threshold].groupby(year_col).size().reset_index(name="count")
    df_simulation_studies_per_year = all_years.merge(df_simulation_studies_per_year, on=year_col, how='left')
    df_simulation_studies_per_year['count'] = df_simulation_studies_per_year['count'].fillna(0).astype(int)

    plt.plot(df_articles_per_year[year_col], df_articles_per_year["count"], label="All Studies", color="black")
    plt.plot(df_simulation_studies_per_year[year_col], df_simulation_studies_per_year["count"], label="Simulation Studies", color="gray")
        
plt.tight_layout()


########### Share of Simulation Studies With Repository
plt.figure(figsize=(10,5))

ctr = 0
for journal in journals:
    ctr+=1
    plt.subplot(3,5,ctr)
    plt.title(journal_names[journal]+"\n("+journal+")", fontsize=9)
    
    df_journal = df_articleinfos_valid[df_articleinfos_valid["journal"]==journal]
    
    df_articles_per_year = df_journal.groupby(year_col).size().reset_index(name='count')
    df_articles_per_year = all_years.merge(df_articles_per_year, on=year_col, how='left')
    df_articles_per_year['count'] = df_articles_per_year['count'].fillna(0).astype(int)

    df_simulation_studies_per_year = df_journal[df_journal[simu_col] >= simulation_threshold].groupby(year_col).size().reset_index(name="count")
    df_simulation_studies_per_year = all_years.merge(df_simulation_studies_per_year, on=year_col, how='left')
    df_simulation_studies_per_year['count'] = df_simulation_studies_per_year['count'].fillna(0).astype(int)

    mask = (df_journal[simu_col] >= simulation_threshold) & (df_journal["has_valid_repository"] == True)
    df_filtered = df_journal[mask]
    df_vrepo_studies_per_year = df_filtered.groupby(year_col).size().reset_index(name="count")
    df_vrepo_studies_per_year = all_years.merge(df_vrepo_studies_per_year, on=year_col, how='left')
    df_vrepo_studies_per_year['count'] = df_vrepo_studies_per_year['count'].fillna(0).astype(int)

    plt.plot(df_simulation_studies_per_year[year_col], df_simulation_studies_per_year["count"], label="Simulation Studies", color="black")
    plt.plot(df_vrepo_studies_per_year[year_col], df_vrepo_studies_per_year["count"], label="Simulation Studies", color="gray")

plt.tight_layout()




###############################################################################
############################## Analysis 4: Simulation Studies with Repository
###############################################################################

