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
import numpy as np
import seaborn as sns




###############################################################################
############################## Constants
###############################################################################
simulation_threshold = 5
year_threshold = 2014

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

df_journal_infos = pd.read_excel("../data/JournalIndex_Top20/Journals_Top20.xlsx")
df_journal_infos = df_journal_infos.dropna()
df_journal_infos["journal"] = "journal_"+df_journal_infos["Nr"].astype(int).astype(str)

df_jif_infos = pd.read_excel("../data/ClarivateJournalCitationReports/JIF_History.xlsx")
del df_jif_infos["Journal"]
df_jif_infos = df_jif_infos.melt(id_vars=['Nr'], 
                              var_name='year', 
                              value_name='value')
df_jif_infos['year'] = df_jif_infos['year'].astype(int)
df_jif_infos = df_jif_infos.sort_values(['Nr', 'year'])
df_jif_infos = df_jif_infos.reset_index(drop=True)
df_jif_infos = df_jif_infos.dropna()

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


df_articleinfos_valid_l5y = df_articleinfos_valid[df_articleinfos_valid[year_col]>=year_threshold]
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
print("Last Five "+str(2024-year_threshold+1)+" ("+str(year_threshold)+" - 2024)")
print(df_articles_journal_summary)




###############################################################################
############################## Analysis 2: Number of Articles & Simulation Studies Over Time
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
plt.subplots_adjust(top=0.84, bottom=0.165)




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
############################## Analysis 4: Reproducibility And Professionality Of Journal
###############################################################################
df_articleinfos_valid_l5y2 = df_articleinfos_valid[df_articleinfos_valid[year_col]>=year_threshold]
df_articleinfos_valid_l5y2 = df_articleinfos_valid_l5y2[df_articleinfos_valid_l5y2[simu_col] >= simulation_threshold]
df_articleinfos_valid_l5y2['repo_score'] = df_articleinfos_valid_l5y2['repo_score'].fillna(0)
df_articleinfos_valid_l5y2 = df_articleinfos_valid_l5y2.merge(df_jif_infos, left_on=["journal", "article_year"], right_on=["Nr", "year"], how="left")
df_articleinfos_valid_l5y2["has_repo"] = df_articleinfos_valid_l5y2["repo_score"]>0
df_articleinfos_valid_l5y2['has_repo'] = df_articleinfos_valid_l5y2['has_repo'].astype(int)

df_articleinfos_valid_l5y3 = df_articleinfos_valid_l5y2[df_articleinfos_valid_l5y2["repo_score"]>0]


# sns.violinplot(y='repo_score', x='value', orient='h', data=df_articleinfos_valid_l5y2)
# plt.xlabel('Journal Impact Factor', fontsize=14)
# plt.ylabel('Repo Score', fontsize=14)
# plt.yticks(range(6), ['0', '1', '2', '3', '4', '5'])  # Ensure all 

# df_articleinfos_valid_l5y2['value_bins'] = pd.cut(df_articleinfos_valid_l5y2['value'], bins=20)
# numeric_columns = df_articleinfos_valid_l5y2.select_dtypes(include=[np.number]).columns
# numeric_columns = numeric_columns.drop(['value'])
# result = df_articleinfos_valid_l5y2.groupby('value_bins')[numeric_columns].mean().reset_index()
# result['value_bins_str'] = result['value_bins'].apply(lambda x: f"{x.mid:.2f}")
# plt.bar(result["value_bins_str"], result["repo_score"])
# plt.xlabel('Journal Impact Factor', fontsize=14)
# plt.ylabel('Av. Repo Score', fontsize=14)

# import sys
# sys.exit(0)



###############################################################################
############################## Analysis 4: Reproducibility And Professionality Of Journal
###############################################################################

# this is all calculated for last 5 years
df_journals_data = df_journal_infos[["journal", "h5-index", "h5-median"]]
df_scatter_journal_data = df_articles_per_journal.copy()
df_scatter_journal_data = df_scatter_journal_data.merge(df_vrepo_studies_per_journal, on="journal", how="left")
df_scatter_journal_data = df_scatter_journal_data.merge(df_journals_data, on="journal", how="left")
df_scatter_journal_data = df_scatter_journal_data.merge(df_simulation_studies_per_journal, on="journal", how="left")
df_scatter_journal_data = df_scatter_journal_data.rename(columns={
    "count_x": "n_articles", 
    "count_y": "n_repo", 
    "count": "n_simstud"
    })
# add article infos
df_articleinfos_valid_l5y = df_articleinfos_valid[df_articleinfos_valid[year_col]>=year_threshold]
df_articleinfos_valid_l5y = df_articleinfos_valid_l5y[df_articleinfos_valid_l5y[simu_col] >= simulation_threshold]
df_articleinfos_valid_l5y = df_articleinfos_valid_l5y[df_articleinfos_valid_l5y["has_valid_repository"]==True]
df_articleinfos_valid_l5y = df_articleinfos_valid_l5y[["journal", year_col, 'has_video',
                                                       'has_code', 'has_dataset', 
                                                       'has_model', 'has_documentation',
                                                       'has_license', 'repo_score']]
article_stats = df_articleinfos_valid_l5y.groupby('journal').agg({
    'has_video': ['sum'], "has_code": ["sum"], "has_dataset": ["sum"], "has_model": ["sum"], "has_documentation": ["sum"], "has_license": ["sum"], "repo_score": ["mean"]
}).reset_index()
article_stats.columns = ['journal', 'n_video', 'n_code', 'n_dataset', 'n_model', 'n_documentation', 'n_license', "av_reposcore"]
df_scatter_journal_data = df_scatter_journal_data.merge(article_stats, on="journal", how="left")

print("Last Five "+str(2024-year_threshold+1)+" ("+str(year_threshold)+" - 2024)")
print(df_scatter_journal_data)

plt.figure(figsize=(10,3))

plt.subplot(1,3,1)
plt.scatter(df_scatter_journal_data["h5-median"], df_scatter_journal_data["n_repo"]/df_scatter_journal_data["n_simstud"]*100, color="black")
plt.xlabel("Journal Impact (h5-median)")
# plt.ylabel("Share of Simulation Studies\nWith Repository [%]")
plt.ylabel("has Repository [%]")

df_scatter_journal_data2 = df_scatter_journal_data.dropna()
df_scatter_journal_data2 = df_scatter_journal_data2.sort_values(by="h5-median", ascending=True)
x = df_scatter_journal_data2["h5-median"]
y = df_scatter_journal_data2["n_repo"]/df_scatter_journal_data2["n_simstud"]*100
z = np.polyfit(x, y, 1)
p = np.poly1d(z)
plt.plot(x, p(x), "--", color="gray")
del df_scatter_journal_data2

plt.subplot(1,3,3)

sns.violinplot(y='repo_score', x='value', orient='h', data=df_articleinfos_valid_l5y2, color='C0')
plt.xlabel('Journal Impact Factor (Crossref)')
plt.ylabel('Repository Score')
plt.yticks(range(6), ['0', '1', '2', '3', '4', '5'])  # Ensure all 
# colors = cm.viridis(np.linspace(0, 1, 6))
# plt.scatter(df_scatter_journal_data["h5-median"], df_scatter_journal_data["n_video"]/df_scatter_journal_data["n_repo"]*100, label="video", color=colors[0])
# plt.scatter(df_scatter_journal_data["h5-median"], df_scatter_journal_data["n_code"]/df_scatter_journal_data["n_repo"]*100, label="code", color=colors[1])
# plt.scatter(df_scatter_journal_data["h5-median"], df_scatter_journal_data["n_dataset"]/df_scatter_journal_data["n_repo"]*100, label="data", color=colors[2])
# plt.scatter(df_scatter_journal_data["h5-median"], df_scatter_journal_data["n_model"]/df_scatter_journal_data["n_repo"]*100, label="model", color=colors[3])
# plt.scatter(df_scatter_journal_data["h5-median"], df_scatter_journal_data["n_documentation"]/df_scatter_journal_data["n_repo"]*100, label="documentation", color=colors[4])
# plt.scatter(df_scatter_journal_data["h5-median"], df_scatter_journal_data["n_license"]/df_scatter_journal_data["n_repo"]*100, label="license", color=colors[5])

# plt.xlabel("Journal Impact (h5-median)")
# plt.ylabel("Share of Repositories [%]")
# plt.legend(loc='upper center', bbox_to_anchor=(0.5, 1.25), ncol=3, fontsize='x-small')

plt.subplot(1,3,2)
# plt.scatter(df_scatter_journal_data["h5-median"], df_scatter_journal_data["av_reposcore"], color="black")
# plt.xlabel("Journal Impact (h5-median)")
# plt.ylabel("Av. Repo Score")

df_articleinfos_valid_l5y2['value_bins'] = pd.cut(df_articleinfos_valid_l5y2['value'], bins=10)
numeric_columns = df_articleinfos_valid_l5y2.select_dtypes(include=[np.number]).columns
numeric_columns = numeric_columns.drop(['value'])
result = df_articleinfos_valid_l5y2.groupby('value_bins')[numeric_columns].mean().reset_index()
result['value_bins_str'] = result['value_bins'].apply(lambda x: f"{x.mid:.2f}")

df_articleinfos_valid_l5y3['value_bins'] = pd.cut(df_articleinfos_valid_l5y3['value'], bins=10)
numeric_columns3 = df_articleinfos_valid_l5y3.select_dtypes(include=[np.number]).columns
numeric_columns3 = numeric_columns3.drop(['value'])
result3 = df_articleinfos_valid_l5y3.groupby('value_bins')[numeric_columns3].mean().reset_index()
result3['value_bins_str'] = result3['value_bins'].apply(lambda x: f"{x.mid:.2f}")

x = np.arange(len(result["value_bins_str"]))
# plt.bar(result["value_bins_str"], result["repo_score"])
plt.bar(result["value_bins_str"], np.asarray(result["has_repo"])*100)
plt.xlabel('Journal Impact Factor (Crossref)')
plt.ylabel('has Repository [%]')

num_ticks = 5  # You can adjust this number to show more or fewer ticks
step = len(result) // (num_ticks - 1)
tick_locations = range(0, len(result), step)
tick_labels = [result["value_bins_str"][i] for i in tick_locations]
plt.xticks(tick_locations, tick_labels, ha='right')

plt.tight_layout()
# plt.subplots_adjust(top=0.835, bottom=0.164, wspace=0.256)
plt.subplots_adjust(top=0.95, bottom=0.164, wspace=0.256)


import sys
sys.exit(0)


###############################################################################
############################## Analysis 5: Reproducibility Over Time
###############################################################################
ly = year_threshold
year_threshold = 2017

mask = (df_articleinfos_valid[simu_col] >= simulation_threshold) & (df_articleinfos_valid["has_valid_repository"] == True)
df_filtered = df_articleinfos_valid[mask]
df_vrepo_studies_per_year = df_filtered.groupby(year_col).size().reset_index(name="count")
df_vrepo_studies_per_year = all_years.merge(df_vrepo_studies_per_year, on=year_col, how='left')
df_vrepo_studies_per_year['count'] = df_vrepo_studies_per_year['count'].fillna(0).astype(int)

df_repo_infos = df_articleinfos_valid.copy()
df_repo_infos = df_repo_infos[df_repo_infos[simu_col] >= simulation_threshold]
df_repo_infos = df_repo_infos[df_repo_infos["has_valid_repository"]==True]
df_repo_infos["rep_score_1"] = df_repo_infos["repo_score"]==1
df_repo_infos["rep_score_2"] = df_repo_infos["repo_score"]==2
df_repo_infos["rep_score_3"] = df_repo_infos["repo_score"]==3
df_repo_infos["rep_score_4"] = df_repo_infos["repo_score"]==4
df_repo_infos["rep_score_5"] = df_repo_infos["repo_score"]==5
df_repo_infos = df_repo_infos[["journal", year_col, 'has_video',
                                                    'has_code', 'has_dataset', 
                                                    'has_model', 'has_documentation',
                                                    'has_license', 'repo_score',
                                                    'rep_score_1', "rep_score_2", "rep_score_3", "rep_score_4", "rep_score_5"]]

article_stats = df_repo_infos.groupby(year_col).agg({
    'has_video': ['sum'], "has_code": ["sum"], "has_dataset": ["sum"], 
    "has_model": ["sum"], "has_documentation": ["sum"], "has_license": ["sum"], "repo_score": ["mean"],
    "rep_score_1": ["sum"], "rep_score_2": ["sum"], "rep_score_3": ["sum"], "rep_score_4": ["sum"], "rep_score_5": ["sum"], 
}).reset_index()
article_stats.columns = [year_col, 'n_video', 'n_code', 'n_dataset', 'n_model', 'n_documentation', 
                         'n_license', "av_reposcore", "n_repo1", "n_repo2", "n_repo3", "n_repo4", "n_repo5"]

df_reprod_time = df_vrepo_studies_per_year.copy()
df_reprod_time = df_reprod_time.merge(article_stats, on=year_col, how="left")
df_reprod_time = df_reprod_time[df_reprod_time[year_col]>=year_threshold]

plt.figure(figsize=(10,3))

plt.subplot(1,3,1)
plt.plot(df_reprod_time[year_col], df_reprod_time["n_video"]/df_reprod_time["count"]*100, label="has video")
plt.plot(df_reprod_time[year_col], df_reprod_time["n_code"]/df_reprod_time["count"]*100, label="has code")
plt.plot(df_reprod_time[year_col], df_reprod_time["n_dataset"]/df_reprod_time["count"]*100, label="has data")
plt.plot(df_reprod_time[year_col], df_reprod_time["n_model"]/df_reprod_time["count"]*100, label="has model")
plt.plot(df_reprod_time[year_col], df_reprod_time["n_documentation"]/df_reprod_time["count"]*100, label="has documentation")
plt.plot(df_reprod_time[year_col], df_reprod_time["n_license"]/df_reprod_time["count"]*100, label="has license")
plt.xlabel("Year")
plt.ylabel("Share Of Simulation Study\nWith Repository [%]")
plt.legend(loc='upper center', bbox_to_anchor=(0.5, 1.3), ncol=3, fontsize='x-small')
plt.ylim(0,100)

plt.subplot(1,3,2)
plt.gca().stackplot(df_reprod_time['article_year'],
             df_reprod_time['n_repo1']/df_reprod_time["count"]*100,
             df_reprod_time['n_repo2']/df_reprod_time["count"]*100,
             df_reprod_time['n_repo3']/df_reprod_time["count"]*100,
             df_reprod_time['n_repo4']/df_reprod_time["count"]*100,
             df_reprod_time['n_repo5']/df_reprod_time["count"]*100,
             labels=['Level 1', 'Level 2', 'Level 3', 'Level 4', 'Level 5'],
             colors=plt.cm.Greys(np.linspace(0.2, 0.8, 5)))
plt.xlabel("Year")
plt.ylabel("Share Of Simulation Study\nWith Repository [%]")
plt.legend(loc='upper center', bbox_to_anchor=(0.5, 1.3), ncol=3, fontsize='x-small')
plt.ylim(0,100)

plt.subplot(1,3,3)
plt.plot(df_reprod_time[year_col], df_reprod_time["av_reposcore"], label="Average Level")
plt.xlabel("Year")
plt.ylabel("Average Repository Level")
plt.ylim(0,5)

plt.tight_layout()
plt.tight_layout()

year_threshold = ly


###############################################################################
############################## Analysis 6: SIMULATION STUDYIES MORE SUCCESSFULL?
###############################################################################

from scipy import stats

df_regression = df_articleinfos_valid.copy()
df_regression_nos = df_regression[df_regression[simu_col] < simulation_threshold]["num_cits_per_year"].dropna()
df_regression_sim = df_regression[df_regression[simu_col] >= simulation_threshold]["num_cits_per_year"].dropna()
df_regression_srp = df_regression[df_regression[simu_col] >= simulation_threshold]
df_regression_srp = df_regression_srp[df_regression_srp["has_repository"]==True]["num_cits_per_year"].dropna()
df_regression_snp = df_regression[df_regression[simu_col] >= simulation_threshold]
df_regression_snp = df_regression_snp[df_regression_snp["has_repository"]==False]["num_cits_per_year"].dropna()

# DESCRIPTION
print("df_regression_sim")
print(pd.DataFrame(df_regression_sim).describe())
print("df_regression_nos")
print(pd.DataFrame(df_regression_nos).describe())
print("df_regression_srp")
print(pd.DataFrame(df_regression_srp).describe())
print("df_regression_snp")
print(pd.DataFrame(df_regression_snp).describe())


# KOLMOGOROV SMIRNOV TEST / CHECK IF NORMALLY DISTRIBUTED
ks_statistic, p_value = stats.kstest(df_regression_sim, 'norm', args=(df_regression_sim.mean(), df_regression_sim.std()))
print(f"K-S Statistic: {ks_statistic}")
print(f"P-value: {p_value}")
alpha = 0.05
if p_value < alpha:
    print("Reject the null hypothesis: The sample does not come from the specified distribution.")
else:
    print("Fail to reject the null hypothesis: The sample may come from the specified distribution.")

# T-TEST that SIM CITATIONS > NO SIM CITATIONS
t_stat, p_value = stats.ttest_ind(df_regression_sim, df_regression_nos, alternative='greater')
print("Sim Studies, av. ",np.nanmean(df_regression_sim))
print("No Sim Studies, av. ",np.nanmean(df_regression_nos))
print(f"T-statistic: {t_stat}")
print(f"P-value (one-sided): {p_value}")
alpha = 0.05  
if p_value < alpha:
    print("Reject the null hypothesis: The mean of 'sim' is significantly greater than 'nos'.")
else:
    print("Fail to reject the null hypothesis: No significant difference in means.")
    
# Mann-Whitney U TEST / WILCOXON RANK SUM TEST
u_statistic, p_value = stats.mannwhitneyu(df_regression_sim, df_regression_nos, alternative='greater')
print(f"Mann-Whitney U Statistic: {u_statistic}")
print(f"P-value: {p_value}")
alpha = 0.05
if p_value < alpha:
    print("Reject the null hypothesis: The mean of 'sim' is significantly greater than 'nos'.")
else:
    print("Fail to reject the null hypothesis: No significant difference in means.")

# KRUSKALL WALLIS H TEST
h_statistic, p_value = stats.kruskal(df_regression_sim, df_regression_nos)
print(f"Kruskal-Wallis H Statistic: {h_statistic}")
print(f"P-value: {p_value}")
alpha = 0.05
if p_value < alpha:
    print("Reject the null hypothesis: At least one group has a different median.")
else:
    print("Fail to reject the null hypothesis: No significant difference in medians.")


###############################################################################
############################## Analysis 6: Regression, Success?
###############################################################################

####### PREPARE REGRESSION TABLE
df_regression = df_articleinfos_valid.copy()
df_regression = df_regression[df_regression[simu_col] >= simulation_threshold]
df_regression = df_regression[df_regression[year_col] >= year_threshold]
df_regression = df_regression[[
    # Dependent Variable
    'num_cits', 'num_cits_per_year', 'num_log_cits', 'num_log_cits_per_year',
    # Fixed Effects
    "journal", "article_year", 
    # Controll Variable
    "num_auths", "num_refs", "num_chars", "num_words",
    # Repository Relevant
    "has_repository", "has_valid_repository", 'repo_score',
    # Detailed Repository Features
    'has_video', 'has_code', 'has_dataset', 'has_model', 'has_documentation',
    'has_license', 
    # Dummy Repository Features
    'dummy_GitHub', 'dummy_GoogleDrive',
    'dummy_YouTube', 'dummy_Zenodo', 'dummy_BitBucket', 'dummy_DropBox',
    'dummy_Mendeley', 'dummy_SourceForge', 'dummy_GoogleDocs'
    ]]
# fillnas with False
cols = ["has_repository", "has_valid_repository",
        'has_video', 'has_code', 'has_dataset', 'has_model', 'has_documentation', 'has_license',
        'dummy_GitHub', 'dummy_GoogleDrive', 'dummy_YouTube', 'dummy_Zenodo', 'dummy_BitBucket', 'dummy_DropBox', 'dummy_Mendeley', 'dummy_SourceForge', 'dummy_GoogleDocs']
for col in cols:
    df_regression[col] = df_regression[col].fillna(False)
    df_regression[col] = df_regression[col].astype(int)
df_regression["repo_score"] = df_regression["repo_score"].fillna(0)
df_regression = df_regression.dropna()
df_regression['journal'] = df_regression['journal'].astype('category')
# filter invalid rows
df_regression_filtered = df_regression[df_regression["num_auths"] != -1]
df_regression_filtered = df_regression[df_regression["num_chars"] != -1]

####### DO DESCRIPTIVE STATISTICS
df_data = df_regression[["num_cits_per_year", "num_log_cits_per_year", "num_auths", "num_refs", "num_chars", "num_words",
                         "has_repository", "has_valid_repository", "repo_score",
                         "has_video", "has_code", "has_dataset", "has_model", "has_documentation", "has_license", 
                         ]]

# Print descriptive statistics
print("Descriptive Statistics:")
df_data_desc = df_data.describe()
print(df_data.describe())

# Print correlation matrix
print("\nCorrelation Matrix:")
df_data_corr = df_data.corr()
print(df_data_corr)


####### DO CORRELATION ANALYSIS

####### DO REGRESSION
from scipy import stats
import statsmodels.api as sm

def doOutlierFiltering(X, Y):
    # Calculate Z-scores of the dependent variable
    z_scores = np.abs(stats.zscore(Y))
    # Identify outliers (Z-score > 3)
    outliers = np.where(z_scores > 3)[0]
    print("Outliers removed: ", len(outliers))
    # Optionally, remove outliers from the dataset
    mask = np.ones(len(Y), dtype=bool)
    mask[outliers] = False
    X = X[mask]
    Y = Y[mask]
    return X, Y
    
def doRegression(df_regression, Y_col, X_cols, fe_year, fe_journal, outlier_filtering):
    # Prepare the data
    Y = df_regression[Y_col]
    X = df_regression[X_cols]
    X = sm.add_constant(X)  # Add a constant term to the model
    # Create entity indicators for fixed effects
    entity_effects = pd.get_dummies(df_regression['journal'], drop_first=True)
    time_effects = pd.get_dummies(df_regression['article_year'], drop_first=True)
    # Combine all variables
    if fe_year and fe_journal:
        X_with_effects = pd.concat([X, entity_effects, time_effects], axis=1)
        bool_columns = X_with_effects.select_dtypes(include=['bool']).columns
        X_with_effects[bool_columns] = X_with_effects[bool_columns].astype(int)
    elif fe_year:
        X_with_effects = pd.concat([X, time_effects], axis=1)
        bool_columns = X_with_effects.select_dtypes(include=['bool']).columns
        X_with_effects[bool_columns] = X_with_effects[bool_columns].astype(int)
    elif fe_journal:
        X_with_effects = pd.concat([X, entity_effects], axis=1)
        bool_columns = X_with_effects.select_dtypes(include=['bool']).columns
        X_with_effects[bool_columns] = X_with_effects[bool_columns].astype(int)
    else:
        X_with_effects = X
    # Outlier Detection using Z-scores
    if outlier_filtering:
        X_with_effects, Y = doOutlierFiltering(X_with_effects, Y)
    
    # OLS Regression
    # model = sm.OLS(Y, X_with_effects)
    # results = model.fit()
    # print(results.summary())
    
    # Negative Binomial Regression
    model = sm.NegativeBinomial(Y, X_with_effects)
    results = model.fit()
    print(results.summary())


print("Model 1")
doRegression(df_regression, 
             # Y_col='num_log_cits_per_year', 
             Y_col='num_cits_per_year', 
             X_cols= ['has_valid_repository', "has_video",
                      'num_auths', 'num_refs'],
             fe_year=False,
             fe_journal=False,
             outlier_filtering=True)

print("Model 2")
doRegression(df_regression, 
             # Y_col='num_log_cits_per_year', 
             Y_col='num_cits_per_year', 
             X_cols= ['has_valid_repository', "has_video",
                      'num_auths', 'num_refs'],
             fe_year=True,
             fe_journal=False,
             outlier_filtering=True)

print("Model 3")
doRegression(df_regression, 
             # Y_col='num_log_cits_per_year', 
             Y_col='num_cits_per_year', 
             X_cols= ['has_valid_repository', "has_video",
                      'num_auths', 'num_refs'],
             fe_year=False,
             fe_journal=True,
             outlier_filtering=True)

print("Model 4")
doRegression(df_regression, 
             # Y_col='num_log_cits_per_year', 
             Y_col='num_cits_per_year', 
             X_cols= ['has_valid_repository', "has_video",
                      'num_auths', 'num_refs'],
             fe_year=True,
             fe_journal=True,
             outlier_filtering=True)

print("Model 5")
doRegression(df_regression, 
             # Y_col='num_log_cits_per_year', 
             Y_col='num_cits_per_year', 
             X_cols= ['has_valid_repository', "has_video",
                      'num_auths', 'num_chars'],
             fe_year=True,
             fe_journal=True,
             outlier_filtering=True)

print("Model 6")
doRegression(df_regression, 
             # Y_col='num_log_cits_per_year', 
             Y_col='num_cits_per_year', 
             X_cols= ["repo_score", "has_video",
                      'num_auths', 'num_refs'],
             fe_year=True,
             fe_journal=True,
             outlier_filtering=True)

print("Model 7")
doRegression(df_regression, 
             # Y_col='num_log_cits_per_year', 
             Y_col='num_cits_per_year', 
             X_cols= ["has_video", "has_code",  
                      'num_auths', 'num_refs'],
             fe_year=True,
             fe_journal=True,
             outlier_filtering=True)

print("Model 8")
doRegression(df_regression, 
             # Y_col='num_log_cits_per_year', 
             Y_col='num_cits_per_year', 
             X_cols= ["has_video", "has_dataset", 
                      'num_auths', 'num_refs'],
             fe_year=True,
             fe_journal=True,
             outlier_filtering=True)
    
print("Model 9")
doRegression(df_regression, 
             # Y_col='num_log_cits_per_year', 
             Y_col='num_cits_per_year', 
             X_cols= ["has_video", "has_model", 
                      'num_auths', 'num_refs'],
             fe_year=True,
             fe_journal=True,
             outlier_filtering=True)

print("Model 10")
doRegression(df_regression, 
             # Y_col='num_log_cits_per_year', 
             Y_col='num_cits_per_year', 
             X_cols= ["has_video", "has_documentation",
                      'num_auths', 'num_refs'],
             fe_year=True,
             fe_journal=True,
             outlier_filtering=True)

print("Model 11")
doRegression(df_regression, 
             # Y_col='num_log_cits_per_year', 
             Y_col='num_cits_per_year', 
             X_cols= ["has_video", "has_license", 
                      'num_auths', 'num_refs'],
             fe_year=True,
             fe_journal=True,
             outlier_filtering=True)


# # Calculate VIF for each predictor variable
# from statsmodels.stats.outliers_influence import variance_inflation_factor  # Correct import
# def calculate_vif(X):
#     vif_data = pd.DataFrame()
#     vif_data["Variable"] = X.columns
#     vif_data["VIF"] = [variance_inflation_factor(X.values, i) for i in range(X.shape[1])]
#     return vif_data
# vif_results = calculate_vif(X_with_effects)
# print(vif_results)



###############################################################################
############################## SUMMARY OF FINDINGs
###############################################################################

# STATEMENTS WE FIND
# 1. Simulation Studies gain growing importance in the field (consistent over all journals).

# 2. Simulation Studies have repositories only in the recent ten years (consistent over all jouranls).

# 3. Simulation Studies with repositories rapidly growing (trend consistent over all journals).

# 4. Does professionality of journal play a role how transparent the studies are in general?
    # generally yes, tendency that more professional usually more transparent
# 4. Does professionality of journal play a role how transparent the studies are per repository feature?
    # no clear relationship visible
    
# 5. Distribution of repository features over time
    # quite constant, not too many differences, slight decrease in reproducibility level

# 6. Does it pay off to be transparent in general?
# 6. Which repository feature most important to pay off?
