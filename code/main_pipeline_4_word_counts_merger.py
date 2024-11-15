###############################################################################
### Author: Kevin Riehl <kriehl@ethz.ch>
### Date: 01.11.2024
### Organization: ETH Zürich, Institute for Transport Planning and Systems (IVT)
### Project: Reproducibility of Simulation Studies in Transportation
###############################################################################
### This file counts the number of words and characters in an article.
###############################################################################




###############################################################################
############################## IMPORTS
###############################################################################
import pandas as pd




###############################################################################
############################## MAIN CODE
###############################################################################

df_j2 = pd.read_csv("../data/pipeline/a_processed_data/journal_2_length.txt", sep="\t", header=None)
df_j3 = pd.read_csv("../data/pipeline/a_processed_data/journal_3_length.txt", sep="\t", header=None)
df_j4 = pd.read_csv("../data/pipeline/a_processed_data/journal_4_length.txt", sep="\t", header=None)
df_j5 = pd.read_csv("../data/pipeline/a_processed_data/journal_5_length.txt", sep="\t", header=None)
df_j6 = pd.read_csv("../data/pipeline/a_processed_data/journal_6_length.txt", sep="\t", header=None)
df_j7 = pd.read_csv("../data/pipeline/a_processed_data/journal_7_length.txt", sep="\t", header=None)
df_j8 = pd.read_csv("../data/pipeline/a_processed_data/journal_8_length.txt", sep="\t", header=None)
df_j9 = pd.read_csv("../data/pipeline/a_processed_data/journal_9_length.txt", sep="\t", header=None)
df_j10 = pd.read_csv("../data/pipeline/a_processed_data/journal_10_length.txt", sep="\t", header=None)
df_j11 = pd.read_csv("../data/pipeline/a_processed_data/journal_11_length.txt", sep="\t", header=None)
df_j13 = pd.read_csv("../data/pipeline/a_processed_data/journal_13_length.txt", sep="\t", header=None)
df_j14 = pd.read_csv("../data/pipeline/a_processed_data/journal_14_length.txt", sep="\t", header=None)
df_j15 = pd.read_csv("../data/pipeline/a_processed_data/journal_15_length.txt", sep="\t", header=None)
df_j17 = pd.read_csv("../data/pipeline/a_processed_data/journal_17_length.txt", sep="\t", header=None)
df_j18 = pd.read_csv("../data/pipeline/a_processed_data/journal_18_length.txt", sep="\t", header=None)

df_complete = pd.concat([df_j2, df_j3, df_j4, df_j5, df_j6, df_j7, df_j8, df_j9, df_j10, df_j11, df_j13, df_j14, df_j15, df_j17, df_j18])
df_complete.columns = ["journal", "article_nr", "n_chars", "n_words"]

df_complete.to_csv("../data/pipeline/b_merged_data/Article_Lengths.csv", index=None)