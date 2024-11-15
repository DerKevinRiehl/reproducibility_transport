# Imports
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.ticker import MaxNLocator


# Methods
def drawQuestionBarPlot(df, question, value_space, xticklabels):
    value_counts = df[question].value_counts()
    counts = value_counts.reindex(value_space, fill_value=0)
    bars = plt.bar(counts.index, counts.values)
    plt.xticks(counts.index)
    for bar in bars:
        height = bar.get_height()
        text = f'{height}'
        text_width, text_height = plt.gca().get_xaxis().get_tick_padding(), plt.gca().get_yaxis().get_tick_padding()
        if height > text_height * 1.2:  # 1.2 is a buffer factor
            plt.text(bar.get_x() + bar.get_width()/2, height/2, text,
                     ha='center', va='center', color="white")
        else:
            plt.text(bar.get_x() + bar.get_width()/2, height, text,
                     ha='center', va='bottom')

    plt.gca().set_xticklabels(xticklabels, ha='right')
    plt.xticks(rotation=45)
    plt.yticks([], [])




# Load Data
df = pd.read_csv("Simulation_Reproducibility_in_Transportation_Science_Submissions.csv")

fig = plt.figure(figsize=(10,3))


position_order = ["Master Student", "PhD / Doctoral Student", "Post-Doc", "Assistant / Junior Professor", "Tenure Track / Senior Professor"]
position = '2) Current Position'
yticklabels = ["Master Student", "PhD Student", "Post-Doc", "Junior Professor", "Senior Professor"]

plt.subplot(2,3,1)
plt.title('Reproducibility As\nSignificant Issue', fontsize=10)

vote = 'The lack of reproducibility in simulation studies is a significant issue in the transportation literature'
dfX = df[[position, vote]]
dfX = dfX.groupby(position)[vote].agg(['mean', 'std']).reset_index()
dfX[position] = pd.Categorical(dfX[position], categories=position_order, ordered=True)
dfX = dfX.sort_values(position)
plt.barh(dfX[position], dfX['mean'], xerr=dfX['std'], capsize=5, error_kw={'ecolor': 'black', 'capthick': 2}, zorder=2)
plt.xlim(1,5.5)
plt.grid(zorder=1)
plt.gca().xaxis.set_major_locator(MaxNLocator(integer=True))
plt.gca().set_yticklabels(yticklabels, ha='right')


plt.subplot(2,3,2)
plt.title('Need For More\nTransparency (Data, Code, Models)', fontsize=10)

vote = 'There is a need for greater transparency from researchers regarding their code, data, and simulation models'
dfX = df[[position, vote]]
dfX = dfX.groupby(position)[vote].agg(['mean', 'std']).reset_index()
dfX[position] = pd.Categorical(dfX[position], categories=position_order, ordered=True)
dfX = dfX.sort_values(position)
plt.barh(dfX[position], dfX['mean'], xerr=dfX['std'], capsize=5, error_kw={'ecolor': 'black', 'capthick': 2}, zorder=2)
plt.xlim(1,5.5)
plt.grid(zorder=1)
plt.yticks([], [])

plt.subplot(2,3,3)
plt.title('Mandatory Data\nAvailability Statement', fontsize=10)

vote = 'Journals should mandate data availability statements and repositories \nto ensure reproducibility (e.g. GitHub, BitBucket, SourceForge, Mendeley) '
dfX = df[[position, vote]]
dfX = dfX.groupby(position)[vote].agg(['mean', 'std']).reset_index()
dfX[position] = pd.Categorical(dfX[position], categories=position_order, ordered=True)
dfX = dfX.sort_values(position)
plt.barh(dfX[position], dfX['mean'], xerr=dfX['std'], capsize=5, error_kw={'ecolor': 'black', 'capthick': 2}, zorder=2)
plt.xlim(1,5.5)
plt.grid(zorder=1)
plt.gca().xaxis.set_major_locator(MaxNLocator(integer=True))
plt.yticks([], [])



# position_order = ["Africa", "Asia", "Australia & Oceania", "Europe", "Middle East", "North America", "South America"]
position = '3) Where is your research organization located?'
# yticklabels = ["Africa", "Asia", "Australia & Oceania", "Europe", "Middle East", "North America", "South America"]

plt.subplot(2,3,1+3)

vote = 'The lack of reproducibility in simulation studies is a significant issue in the transportation literature'
dfX = df[[position, vote]]
dfX = dfX.groupby(position)[vote].agg(['mean', 'std']).reset_index()
# dfX[position] = pd.Categorical(dfX[position], categories=position_order, ordered=True)
dfX = dfX.sort_values(position)
plt.barh(dfX[position], dfX['mean'], xerr=dfX['std'], capsize=5, error_kw={'ecolor': 'black', 'capthick': 2}, zorder=2)
plt.xlim(1,5.5)
plt.grid(zorder=1)
plt.gca().xaxis.set_major_locator(MaxNLocator(integer=True))
# plt.gca().set_yticklabels(yticklabels, ha='right')


plt.subplot(2,3,2+3)

vote = 'There is a need for greater transparency from researchers regarding their code, data, and simulation models'
dfX = df[[position, vote]]
dfX = dfX.groupby(position)[vote].agg(['mean', 'std']).reset_index()
# dfX[position] = pd.Categorical(dfX[position], categories=position_order, ordered=True)
dfX = dfX.sort_values(position)
plt.barh(dfX[position], dfX['mean'], xerr=dfX['std'], capsize=5, error_kw={'ecolor': 'black', 'capthick': 2}, zorder=2)
plt.xlim(1,5.5)
plt.grid(zorder=1)
plt.yticks([], [])

plt.subplot(2,3,3+3)

vote = 'Journals should mandate data availability statements and repositories \nto ensure reproducibility (e.g. GitHub, BitBucket, SourceForge, Mendeley) '
dfX = df[[position, vote]]
dfX = dfX.groupby(position)[vote].agg(['mean', 'std']).reset_index()
# dfX[position] = pd.Categorical(dfX[position], categories=position_order, ordered=True)
dfX = dfX.sort_values(position)
plt.barh(dfX[position], dfX['mean'], xerr=dfX['std'], capsize=5, error_kw={'ecolor': 'black', 'capthick': 2}, zorder=2)
plt.xlim(1,5.5)
plt.grid(zorder=1)
plt.gca().xaxis.set_major_locator(MaxNLocator(integer=True))
plt.yticks([], [])



plt.tight_layout()