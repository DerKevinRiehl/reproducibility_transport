# Imports
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D



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
df = pd.read_csv("Simulation_Reproducibility_in_Transportation_Science_Submissions_2024-11-05.csv")
value_space = [1,2,3,4,5]


# Draw Figure
fig = plt.figure(figsize=(10,3))

plt.subplot(1,3,1)
plt.title('Research Experience', fontsize=10)
drawQuestionBarPlot(df, 
                    question='1) Research Experience', 
                    value_space=["1-2", "2-3", "3-4", "5-10", "10+"],
                    xticklabels=["1-2", "2-3", "3-4", "5-10", "10+"])

plt.subplot(1,3,2)
plt.title('Position', fontsize=10)
drawQuestionBarPlot(df, 
                    question='2) Current Position', 
                    value_space=["Master Student", "PhD / Doctoral Student", "Post-Doc", "Assistant / Junior Professor", "Tenure Track / Senior Professor"], 
                    xticklabels=["Master Student", "PhD Student", "Post-Doc", "Junior Professor", "Senior Professor"])

plt.subplot(1,3,3)
plt.title('Region', fontsize=10)
drawQuestionBarPlot(df, 
                    question='3) Where is your research organization located?', 
                    value_space=["Africa", "Asia", "Australia & Oceania", "Europe", "Middle East", "North America", "South America"], 
                    xticklabels=["Africa", "Asia", "Australia & Oceania", "Europe", "Middle East", "North America", "South America"])

plt.tight_layout()
plt.subplots_adjust(top=0.9, hspace=0.45)  # Adjust top margin and space between rows
