# Imports
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D



# Methods
def drawQuestionBarPlot(df, question):
    value_counts = df[question].value_counts()
    average = np.mean(df[question])
    counts = value_counts.reindex(value_space, fill_value=0)
    bars = plt.bar(counts.index, counts.values)
    plt.xticks(counts.index)
    # Add average text in top left corner
    plt.text(0.05, 0.95, f'Avg: {average:.2f}', 
             transform=plt.gca().transAxes, 
             fontsize=10, fontweight='bold', 
             verticalalignment='top',
             bbox=dict(facecolor='white', alpha=0.7, edgecolor='none', pad=2))
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
    plt.axvline(x=average, color='black', linestyle='--', label=f'Average: {average:.2f}')

    plt.xticks([], [])
    plt.yticks([], [])

def drawQuestionBarPlotYesNo(df, question):
    n_yes = sum(df[question]=="Yes")
    n_no = sum(df[question]=="No")
    
    # Create data for the bar plot
    categories = ['Yes', 'No']
    values = [n_yes, n_no]
    colors = ['tab:blue', 'tab:blue']
    
    # Create the bar plot
    bars = plt.bar(categories, values, color=colors)
    plt.xticks(categories)
    
    # Add average text in top left corner
    # plt.text(0.05, 0.95, f'Yes: {average:.0f}%', 
    #          transform=plt.gca().transAxes, 
    #          fontsize=10, fontweight='bold', 
    #          verticalalignment='top',
    #          bbox=dict(facecolor='white', alpha=0.7, edgecolor='none', pad=3))
    
    # Add value labels on the bars
    ctr = 0
    for bar in bars:
        height = bar.get_height()
        if ctr==0:
            average = n_yes/(n_yes+n_no)*100
            plt.text(bar.get_x() + bar.get_width()/2, height/4,
                     f'Yes [{n_yes}]\n{average:.0f}%',
                     ha='center', va='bottom', color="white")
            ctr=1
        else:
            average = n_no/(n_yes+n_no)*100
            plt.text(bar.get_x() + bar.get_width()/2, height/2,
                     f'No [{n_no}]\n{average:.0f}%',
                     ha='center', va='bottom', color="white")
    
    # Set y-axis to start at 0
    plt.ylim(bottom=0)
    
    plt.xticks([], [])
    plt.yticks([], [])
    

def drawDoubleQuestionBarPlot(df, question1, question2):
    value_counts1 = df[question1].value_counts()
    value_counts2 = df[question2].value_counts()
    average1 = np.mean(df[question1])
    average2 = np.mean(df[question2])
    
    counts1 = value_counts1.reindex(value_space, fill_value=0)
    counts2 = value_counts2.reindex(value_space, fill_value=0)
    
    x = np.arange(len(value_space))
    width = 0.35
    
    bars1 = plt.bar(x - width/2, counts1.values, width, color='tab:blue', label=f"Me [{average1:.2f}]")
    bars2 = plt.bar(x + width/2, counts2.values, width, color='tab:green', label=f"Others [{average2:.2f}]")
    
    plt.xticks(x, value_space)
    
    def add_labels(bars):
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
    
    add_labels(bars1)
    add_labels(bars2)
    
    plt.axvline(x=average1-1, color='black', linestyle='--')#, label=f"Me [{average1:.2f}]")
    plt.axvline(x=average2-1, color='black', linestyle=':')#, label=f"Others [{average2:.2f}]")
    
    plt.legend(fontsize='x-small', ncol=2, loc='upper right', bbox_to_anchor=(1, 1.02))
    
    plt.xticks([], [])
    plt.yticks([], [])

# Load Data
df = pd.read_csv("Simulation_Reproducibility_in_Transportation_Science_Submissions_2024-11-05.csv")
value_space = [1,2,3,4,5]


# Draw Figure
fig = plt.figure(figsize=(10,7))

# Title for the first row
# fig.text(0.5, 0.97, '(1/3) Perceived Severity of Reproducibility As An Issue', 
         # ha='center', va='center', fontsize=14, fontweight='bold')

# Title for the second row
# fig.text(0.5, 0.62, '(2/3) Factors Influencing Transparency Of Authors', 
         # ha='center', va='center', fontsize=14, fontweight='bold')

# Page 1: Assessing Simulation Reproducibility in Transportation Research
plt.subplot(5,4,1)
plt.title('Q1.1: Reproducibility As\nSignificant Issue', fontsize=10)
drawQuestionBarPlot(df, question="The lack of reproducibility in simulation studies is a significant issue in the transportation literature")

plt.subplot(5,4,2)
plt.title('Q1.2: Spent Unnecessary\nEfforts To Reproduce', fontsize=10)
drawQuestionBarPlot(df, question="I have invested considerable time and effort in attempting to reproduce existing studies (which could have been avoided, e.g. with better documentation)")

plt.subplot(5,4,3)
plt.title('Q1.3: Need For More\nTransparency (Data, Code, Models)', fontsize=10)
drawQuestionBarPlot(df, question="There is a need for greater transparency from researchers regarding their code, data, and simulation models")

plt.subplot(5,4,4)
plt.title('Q1.4: Mandatory Data\nAvailability Statement', fontsize=10)
drawQuestionBarPlot(df, question="New publications should be required to include a basic online repository and data availability statement")

# Page 2: Factory Influencing Transparency
plt.subplot(5,4,5)
plt.title('Q2.1: Legal Constraints', fontsize=10)
drawQuestionBarPlot(df, question="I cannot publish due to legal constraints (e.g., data privacy, intellectual property rights)")

plt.subplot(5,4,6)
plt.title('Q2.2: Quality Concerns', fontsize=10)
drawQuestionBarPlot(df, question="I have concerns about the quality of reliability of my simulations")

plt.subplot(5,4,7)
plt.title('Q2.3: Lack of Confidence', fontsize=10)
drawQuestionBarPlot(df, question="I lack confidence and/or feel vulnerable in sharing code, data, or models publicly")
   
plt.subplot(5,4,8)
plt.title('Q2.4: Time Constraints', fontsize=10)
drawQuestionBarPlot(df, question="I have time constraints (that limit efforts in preparing repositories and managing data-sharing agreements to the desired level)")
    
plt.subplot(5,4,9)
plt.title('Q2.5: Lack of Knowledge', fontsize=10)
drawQuestionBarPlot(df, question='I lack knowledge about tools and best practices for managing repositories')
   
plt.subplot(5,4,10)
plt.title('Q2.6: Upon Request\nIs Sufficient', fontsize=10)
drawQuestionBarPlot(df, question='I believe sharing data upon request is sufficient (e.g., via email)')
   
plt.subplot(5,4,11)
plt.title('Q2.7: Fear Reduced Chances\nOf Publication', fontsize=10)
drawDoubleQuestionBarPlot(df, 'I fear transparency might hinder chances of publication acceptance',
                              'Other researchers fear transparency might hinder chances of publication acceptance')
          
plt.subplot(5,4,12)
plt.title('Q2.8: Intentionally To\nMaintain Advantage', fontsize=10)
drawDoubleQuestionBarPlot(df, 'I intentionally withhold materials to maintain a competitive advantage',
                              'Other researchers intentionally withhold materials to maintain what they believe to be a competitive advantage')
      
# Page 3: Suggestions / Strategies To Improve
plt.subplot(5,4,13)
plt.title('Q3.1: Publish Data', fontsize=10)
drawQuestionBarPlot(df, question="Researchers should publish data (raw or processed)")
         
plt.subplot(5,4,14)
plt.title('Q3.2: Publish Models', fontsize=10)
drawQuestionBarPlot(df, question="Researchers should publish simulation models")
         
plt.subplot(5,4,15)
plt.title('Q3.3: Publish Software Code', fontsize=10)
drawQuestionBarPlot(df, question="Researchers should publish software / source code")
         
plt.subplot(5,4,16)
plt.title('Q3.4: Publish Online Appendix', fontsize=10)
drawQuestionBarPlot(df, question="Researchers should publish a comprehensive online appendix alongside each study, detailing the methodologies")
         
plt.subplot(5,4,17)
plt.title('Q3.5: Data\nAvailability Statement', fontsize=10)
drawQuestionBarPlot(df, question="Journals should mandate data availability statements and repositories \nto ensure reproducibility (e.g. GitHub, BitBucket, SourceForge, Mendeley) ")
         
plt.subplot(5,4,18)
plt.title('Q3.6: Funding Agencies\nShould Require Strategy', fontsize=10)
drawQuestionBarPlot(df, question="Funding agencies should require detailed reproducibility plans in grant proposals")
  
plt.subplot(5,4,19)
plt.title('Q3.7: Research Group\nImplemented Strategy', fontsize=10)
drawQuestionBarPlotYesNo(df, question="Our research group has implemented some type of measure to enhance reproducibility in our work")

plt.tight_layout()
plt.subplots_adjust(top=0.9, hspace=0.45)  # Adjust top margin and space between rows

# # After all subplots are created, add the horizontal lines
fig.add_subplot(111, frameon=False)
plt.tick_params(labelcolor='none', top=False, bottom=False, left=False, right=False)

# # Line after the first row
plt.axhline(y=0.83, color='black', linestyle='-', linewidth=2.5)

# # Line after the third row
plt.axhline(y=0.4, color='black', linestyle='-', linewidth=2.5)
