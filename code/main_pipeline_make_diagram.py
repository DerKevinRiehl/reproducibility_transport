###############################################################################
############################## Imports
###############################################################################
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt




###############################################################################
############################## Mehtods
###############################################################################

def checkConsistency(df_git, platform):
    # Filter articles where 'github' is in the lowercase 'url' field
    github_articles = df_git[df_git['url'].str.lower().str.contains(platform, na=False)]   
    # Count articles per year
    github_count = github_articles.groupby('year').size().reset_index(name='count')
    # Merge the all_years DataFrame with the github_count DataFrame
    github_count = all_years.merge(github_count, on='year', how='left')
    # Fill NaN values with 0 and ensure 'count' is integer type
    github_count['count'] = github_count['count'].fillna(0).astype(int)
    # Sort the result by year in ascending order
    github_count = github_count.sort_values('year')
    return github_count




###############################################################################
############################## Load DataFrames
###############################################################################
df_git = pd.read_excel("Journal_2_final.xlsx")
df_keyw = pd.read_excel("Journal_2_keywords.xlsx")
df_arti = pd.read_excel("Journal_2_articleInfos.xlsx")
df_keyw = df_keyw.merge(df_arti, on=["journal", "article_nr"])

all_years = pd.DataFrame({'year': range(2000, 2025)})
df_articles_per_year = df_arti.groupby('year').size().reset_index(name='count')
df_articles_per_year = all_years.merge(df_articles_per_year, on='year', how='left')
df_articles_per_year['count'] = df_articles_per_year['count'].fillna(0).astype(int)






###############################################################################
############################## Plot About Talking About Simulations
###############################################################################

plt.figure(figsize=(15,12))

plt.subplot(2,2,1)
plt.title("simulation")
plt.plot(df_articles_per_year["year"], df_articles_per_year["count"])
for x in range(1,10):
    df_simulation_count = df_keyw[df_keyw['simulation'] > x].groupby('year').size().reset_index(name='count')
    df_simulation_count = all_years.merge(df_simulation_count, on='year', how='left')
    df_simulation_count['count'] = df_simulation_count['count'].fillna(0).astype(int)
    plt.plot(df_simulation_count["year"], df_simulation_count["count"], label=str(x))

plt.subplot(2,2,2)
plt.title("Journal 2")
for x in range(1,10):
    df_simulation_count = df_keyw[df_keyw['simulation'] > x].groupby('year').size().reset_index(name='count')
    df_simulation_count = all_years.merge(df_simulation_count, on='year', how='left')
    df_simulation_count['count'] = df_simulation_count['count'].fillna(0).astype(int)
    plt.plot(df_simulation_count["year"], df_simulation_count["count"]/df_articles_per_year["count"], label=str(x))

plt.subplot(2,2,3)
plt.title("repository")
plt.plot(df_articles_per_year["year"], df_articles_per_year["count"])
for x in range(1,10):
    df_repository_count = df_keyw[df_keyw['repository'] > x].groupby('year').size().reset_index(name='count')
    df_repository_count = all_years.merge(df_repository_count, on='year', how='left')
    df_repository_count['count'] = df_repository_count['count'].fillna(0).astype(int)
    plt.plot(df_repository_count["year"], df_repository_count["count"], label=str(x))

plt.subplot(2,2,4)
plt.title("Journal 2")
for x in range(1,10):
    df_repository_count = df_keyw[df_keyw['repository'] > x].groupby('year').size().reset_index(name='count')
    df_repository_count = all_years.merge(df_repository_count, on='year', how='left')
    df_repository_count['count'] = df_repository_count['count'].fillna(0).astype(int)
    plt.plot(df_repository_count["year"], df_repository_count["count"]/df_articles_per_year["count"], label=str(x))

plt.legend()
plt.tight_layout()





###############################################################################
############################## Plot About Actual URL Provision
###############################################################################

df_simulation_count = df_keyw[df_keyw['simulation'] > 2].groupby('year').size().reset_index(name='count')
df_simulation_count = all_years.merge(df_simulation_count, on='year', how='left')
df_simulation_count['count'] = df_simulation_count['count'].fillna(0).astype(int)

simulation_articles_nr_list = df_keyw[df_keyw['simulation'] > 2]['article_nr'].unique()
print(len(df_git))
df_git2 = df_git[df_git["article_nr"].isin(simulation_articles_nr_list)]
print(len(df_git2))

df_github = checkConsistency(df_git2, "github")
df_googledrive = checkConsistency(df_git2, "drive.google")
df_bitbucket = checkConsistency(df_git2, "bitbucket")
df_sourceforge = checkConsistency(df_git2, "sourceforge")

df_articles_with_repos = df_git2.groupby("year").size().reset_index(name="count")
df_articles_with_repos = all_years.merge(df_articles_with_repos, on='year', how='left')
df_articles_with_repos['count'] = df_articles_with_repos['count'].fillna(0).astype(int)


plt.figure(figsize=(15,12))

plt.subplot(2,1,1)
plt.title("Absolute Number of Simulation-Study Papers with GitHub")
plt.plot(df_articles_with_repos["year"], df_articles_with_repos["count"])

plt.subplot(2,1,2)
plt.title("Relative Number of Simulation-Study Papers with GitHub From All Simulation-Study-Papers")
plt.plot(df_articles_with_repos["year"], df_articles_with_repos["count"]/df_simulation_count["count"])





###############################################################################
############################## Plot About What Repositories are used
###############################################################################

plt.figure(figsize=(12, 6))
plt.stackplot(df_github["year"],
              df_github['count'],
              df_googledrive['count'],
              df_bitbucket['count'],
              df_sourceforge['count'],
              labels=['GitHub', 'Google Drive', 'Bitbucket', 'SourceForge'])

plt.subplot(1,2,1)
plt.xlabel('Year')
plt.ylabel('Count')
plt.title('Repository Usage Over Time')
plt.legend(loc='upper left')
plt.xlim(2000, 2024)
plt.xticks(range(2000, 2025, 2), rotation=45)


plt.subplot(1,2,2)
df_combined = pd.DataFrame({
    'year': df_github['year'],
    'GitHub': df_github['count'],
    'Google Drive': df_googledrive['count'],
    'Bitbucket': df_bitbucket['count'],
    'SourceForge': df_sourceforge['count']
})

# Calculate percentages
df_percentages = df_combined.set_index('year')
df_percentages = df_percentages.div(df_percentages.sum(axis=1), axis=0) * 100

plt.stackplot(df_github['year'],
              df_percentages['GitHub'],
              df_percentages['Google Drive'],
              df_percentages['Bitbucket'],
              df_percentages['SourceForge'],
              labels=['GitHub', 'Google Drive', 'Bitbucket', 'SourceForge'])

plt.xlabel('Year')
plt.ylabel('Percentage')
plt.title('Relative Repository Usage Over Time')
plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
plt.xlim(2000, 2024)
plt.ylim(0, 100)
plt.xticks(range(2000, 2025, 2), rotation=45)

# Add gridlines for better readability
plt.grid(True, linestyle='--', alpha=0.7)

# Add percentage labels on y-axis
plt.yticks(range(0, 101, 20), [f'{i}%' for i in range(0, 101, 20)])

plt.tight_layout()
plt.show()