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
all_years = pd.DataFrame({'year': range(2000, 2024)})
simulation_threshold = 5

df_articleinfos = pd.read_excel("b_merged_data/ArticleInfos_manual.xlsx")
df_articlerepos = pd.read_excel("b_merged_data/ArticleURLs.xlsx")
df_articleinfos_valid = df_articleinfos.copy()
df_articleinfos_valid = df_articleinfos_valid[df_articleinfos_valid["year"].notna()]

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



###############################################################################
############################## Analysis 1: Table Number Articles And Simulations Per Journal
###############################################################################

df_articles_per_journal = df_articleinfos_valid.groupby('journal').size().reset_index(name='count')
df_simulation_studies_per_journal = df_articleinfos_valid[df_articleinfos_valid["simulation"] > simulation_threshold].groupby("journal").size().reset_index(name="count")

df_articles_journal_summary = df_articles_per_journal.copy()
df_articles_journal_summary = df_articles_journal_summary.merge(df_simulation_studies_per_journal, on="journal", how="left")
df_articles_journal_summary["ratio"] = df_articles_journal_summary["count_y"]/df_articles_journal_summary["count_x"]
df_articles_journal_summary = df_articles_journal_summary[["journal", "count_y", "count_x", "ratio"]]
print(df_articles_journal_summary)


###############################################################################
############################## Analysis 1: Number of Articles & Simulation Studies
###############################################################################

df_articles_per_year = df_articleinfos_valid.groupby('year').size().reset_index(name='count')
df_articles_per_year = all_years.merge(df_articles_per_year, on='year', how='left')
df_articles_per_year['count'] = df_articles_per_year['count'].fillna(0).astype(int)

df_simulation_studies_per_year = df_articleinfos_valid[df_articleinfos_valid["simulation"] > simulation_threshold].groupby("year").size().reset_index(name="count")
df_simulation_studies_per_year = all_years.merge(df_simulation_studies_per_year, on='year', how='left')
df_simulation_studies_per_year['count'] = df_simulation_studies_per_year['count'].fillna(0).astype(int)


plt.figure(figsize=(10,3))
# plt.suptitle("Transportation Literature Corpus")

plt.subplot(1,2,1)
plt.title("Number of Studies")
plt.plot(df_articles_per_year["year"], df_articles_per_year["count"], label="All Studies", color="black")
plt.plot(df_simulation_studies_per_year["year"], df_simulation_studies_per_year["count"], label="Simulation Studies", color="gray")
plt.xlabel("Years")
plt.ylabel("Number of Articles")
plt.legend()

plt.subplot(1,2,2)
plt.title("Share of Simulation Studies")
plt.plot(df_simulation_studies_per_year["year"], df_simulation_studies_per_year["count"]/df_articles_per_year["count"]*100, label="Simulation Studies", color="blue")
plt.xlabel("Years")
plt.ylabel("Share of All Articles [%]")

plt.tight_layout()


###############################################################################
############################## Analysis 1: Number of Articles & Simulation Studies Per Journal
###############################################################################

plt.figure(figsize=(10,5))

ctr = 0
for journal in journals:
    ctr+=1
    plt.subplot(3,5,ctr)
    plt.title(journal_names[journal]+"\n("+journal+")", fontsize=9)
    # plt.title(journal)
    
    df_journal = df_articleinfos_valid[df_articleinfos_valid["journal"]==journal]
    
    df_articles_per_year = df_journal.groupby('year').size().reset_index(name='count')
    df_articles_per_year = all_years.merge(df_articles_per_year, on='year', how='left')
    df_articles_per_year['count'] = df_articles_per_year['count'].fillna(0).astype(int)

    df_simulation_studies_per_year = df_journal[df_journal["simulation"] > simulation_threshold].groupby("year").size().reset_index(name="count")
    df_simulation_studies_per_year = all_years.merge(df_simulation_studies_per_year, on='year', how='left')
    df_simulation_studies_per_year['count'] = df_simulation_studies_per_year['count'].fillna(0).astype(int)

    plt.plot(df_articles_per_year["year"], df_articles_per_year["count"], label="All Studies", color="black")
    plt.plot(df_simulation_studies_per_year["year"], df_simulation_studies_per_year["count"], label="Simulation Studies", color="gray")
        
plt.tight_layout()



###############################################################################
############################## Analysis 2: Simulation Studies with Repository
###############################################################################

df_simulation_studies = df_articleinfos_valid[df_articleinfos_valid["simulation"] > simulation_threshold]