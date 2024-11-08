###############################################################################
### Author: Kevin Riehl <kriehl@ethz.ch>
### Date: 01.11.2024
### Organization: ETH Zürich, Institute for Transport Planning and Systems (IVT)
### Project: Reproducibility of Simulation Studies in Transportation
###############################################################################
### This file merges the single files per journal into one large file.
### Two outputs are created: 
###    - ArticleInfos.xlsx  (containing an overview of all downloaded articles and metadata)
###    - ArticleURLs.xlsx   (containing a list of all "relevant" repository URLs found in the articles)
### The ArticleInfos were manually corected were metadata could not be found, and as a result modified file exists:
###    - ArticleInfos_Manual.xlsx
###    - ArticleInfos_URLs_manual_1.xlsx
###    - ArticleInfos_URLs_manual_2.xlsx
### Furthermore the found repositories were manually investigated
###    - Repository_Review_manual.xlsx
###############################################################################



###############################################################################
############################## Imports
###############################################################################
import pandas as pd




###############################################################################
############################## Merge ArticleInfos
###############################################################################

df_j2_a = pd.read_excel("a_processed_data/journal_2_keywords.xlsx")
df_j2_b = pd.read_excel("a_processed_data/journal_2_articleInfos.xlsx")
df_j2 = df_j2_b.merge(df_j2_a, on=["journal", "article_nr"], how="left")
del df_j2['Unnamed: 0_x']
del df_j2['Unnamed: 0_y']

df_j3_a = pd.read_excel("a_processed_data/journal_3_keywords.xlsx")
df_j3_b = pd.read_excel("a_processed_data/journal_3_articleInfos.xlsx")
df_j3 = df_j3_b.merge(df_j3_a, on=["journal", "article_nr"], how="left")
del df_j3['Unnamed: 0_x']
del df_j3['Unnamed: 0_y']

df_j4_a = pd.read_excel("a_processed_data/journal_4_keywords.xlsx")
df_j4_b = pd.read_excel("a_processed_data/journal_4_articleInfos.xlsx")
df_j4 = df_j4_b.merge(df_j4_a, on=["journal", "article_nr"], how="left")
del df_j4['Unnamed: 0_x']
del df_j4['Unnamed: 0_y']

df_j5_a = pd.read_excel("a_processed_data/journal_5_keywords.xlsx")
df_j5_b = pd.read_excel("a_processed_data/journal_5_articleInfos.xlsx")
df_j5 = df_j5_b.merge(df_j5_a, on=["journal", "article_nr"], how="left")
del df_j5['Unnamed: 0_x']
del df_j5['Unnamed: 0_y']

df_j6_a = pd.read_excel("a_processed_data/journal_6_keywords.xlsx")
df_j6_b = pd.read_excel("a_processed_data/journal_6_articleInfos.xlsx")
df_j6 = df_j6_b.merge(df_j6_a, on=["journal", "article_nr"], how="left")
del df_j6['Unnamed: 0_x']
del df_j6['Unnamed: 0_y']

df_j7_a = pd.read_excel("a_processed_data/journal_7_keywords.xlsx")
df_j7_b = pd.read_excel("a_processed_data/journal_7_articleInfos.xlsx")
df_j7 = df_j7_b.merge(df_j7_a, on=["journal", "article_nr"], how="left")
del df_j7['Unnamed: 0_x']
del df_j7['Unnamed: 0_y']

df_j8_a = pd.read_excel("a_processed_data/journal_8_keywords.xlsx")
df_j8_b = pd.read_excel("a_processed_data/journal_8_articleInfos.xlsx")
df_j8 = df_j8_b.merge(df_j8_a, on=["journal", "article_nr"], how="left")
del df_j8['Unnamed: 0_x']
del df_j8['Unnamed: 0_y']

df_j9_a = pd.read_excel("a_processed_data/journal_9_keywords.xlsx")
df_j9_b = pd.read_excel("a_processed_data/journal_9_articleInfos.xlsx")
df_j9 = df_j9_b.merge(df_j9_a, on=["journal", "article_nr"], how="left")
del df_j9['Unnamed: 0_x']
del df_j9['Unnamed: 0_y']

df_j10_a = pd.read_excel("a_processed_data/journal_10_keywords.xlsx")
df_j10_b = pd.read_excel("a_processed_data/journal_10_articleInfos.xlsx")
df_j10 = df_j10_b.merge(df_j10_a, on=["journal", "article_nr"], how="left")
del df_j10['Unnamed: 0_x']
del df_j10['Unnamed: 0_y']

df_j11_a = pd.read_excel("a_processed_data/journal_11_keywords.xlsx")
df_j11_b = pd.read_excel("a_processed_data/journal_11_articleInfos.xlsx")
df_j11 = df_j11_b.merge(df_j11_a, on=["journal", "article_nr"], how="left")
del df_j11['Unnamed: 0_x']
del df_j11['Unnamed: 0_y']

df_j13_a = pd.read_excel("a_processed_data/journal_13_keywords.xlsx")
df_j13_b = pd.read_excel("a_processed_data/journal_13_articleInfos.xlsx")
df_j13 = df_j13_b.merge(df_j13_a, on=["journal", "article_nr"], how="left")
del df_j13['Unnamed: 0_x']
del df_j13['Unnamed: 0_y']

df_j14_a = pd.read_excel("a_processed_data/journal_14_keywords.xlsx")
df_j14_b = pd.read_excel("a_processed_data/journal_14_articleInfos.xlsx")
df_j14 = df_j14_b.merge(df_j14_a, on=["journal", "article_nr"], how="left")
del df_j14['Unnamed: 0_x']
del df_j14['Unnamed: 0_y']

df_j15_a = pd.read_excel("a_processed_data/journal_15_keywords.xlsx")
df_j15_b = pd.read_excel("a_processed_data/journal_15_articleInfos.xlsx")
df_j15 = df_j15_b.merge(df_j15_a, on=["journal", "article_nr"], how="left")
del df_j15['Unnamed: 0_x']
del df_j15['Unnamed: 0_y']

df_j17_a = pd.read_excel("a_processed_data/journal_17_keywords.xlsx")
df_j17_b = pd.read_excel("a_processed_data/journal_17_articleInfos.xlsx")
df_j17 = df_j17_b.merge(df_j17_a, on=["journal", "article_nr"], how="left")
del df_j17['Unnamed: 0_x']
del df_j17['Unnamed: 0_y']

df_j18_a = pd.read_excel("a_processed_data/journal_18_keywords.xlsx")
df_j18_b = pd.read_excel("a_processed_data/journal_18_articleInfos.xlsx")
df_j18 = df_j18_b.merge(df_j18_a, on=["journal", "article_nr"], how="left")
del df_j18['Unnamed: 0_x']
del df_j18['Unnamed: 0_y']

df_complete = pd.concat((df_j2, df_j3, df_j4, df_j5, df_j6, df_j7, df_j8, df_j9, df_j10, df_j11, df_j13, df_j14, df_j15, df_j17, df_j18))
df_complete.to_excel("b_merged_data/ArticleInfos.xlsx")




###############################################################################
############################## Merge Repository URLs
###############################################################################

df_j2 = pd.read_excel("a_processed_data/journal_2_final.xlsx")
df_j3 = pd.read_excel("a_processed_data/journal_3_final.xlsx")
df_j4 = pd.read_excel("a_processed_data/journal_4_final.xlsx")
df_j5 = pd.read_excel("a_processed_data/journal_5_final.xlsx")
df_j6 = pd.read_excel("a_processed_data/journal_6_final.xlsx")
df_j7 = pd.read_excel("a_processed_data/journal_7_final.xlsx")
df_j8 = pd.read_excel("a_processed_data/journal_8_final.xlsx")
df_j9 = pd.read_excel("a_processed_data/journal_9_final.xlsx")
df_j10 = pd.read_excel("a_processed_data/journal_10_final.xlsx")
df_j11 = pd.read_excel("a_processed_data/journal_11_final.xlsx")
df_j13 = pd.read_excel("a_processed_data/journal_13_final.xlsx")
df_j14 = pd.read_excel("a_processed_data/journal_14_final.xlsx")
df_j15 = pd.read_excel("a_processed_data/journal_15_final.xlsx")
df_j17 = pd.read_excel("a_processed_data/journal_17_final.xlsx")
df_j18 = pd.read_excel("a_processed_data/journal_18_final.xlsx")

df_complete = pd.concat((df_j2, df_j3, df_j4, df_j5, df_j6, df_j7, df_j8, df_j9, df_j10, df_j11, df_j13, df_j14, df_j15, df_j17, df_j18))
df_complete.to_excel("b_merged_data/ArticleURLs.xlsx")

