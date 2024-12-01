# Simulation study reproducibility - an inventory & recommendations for the field of transportation

In this repository you can find the source code used to render the transportation simulation study article corpus dataset, to analyse the survey outcome, and to empirically assess the article corpus dataset.  

All scripts are developed with Python 3.9 and serve as documentation of the specific analysis steps. Additional software packages and versions can be found in `requirements.txt`.


## Overview of Available Dataset

- `ArticleInformation` this folder contains two Excel sheets with all meta data information on the article corpus dataset and the manually reviewed repositories mentioned within.
- `ClarivateJournalCitationReports` this folder contains the journal impact factors for the period of time and journals relevant to this study.
- `JournalIndex_Top20` this folder contains two Excel sheets about all the articles and journals that belong to the top 20 journals of the field. (this includes articles that were not downloaded, or for which no additional meta data could be retrieved as well)
- `pipeline` this folder contains data of several steps of the processing pipeline outlined below. The folder with all downloaded articles in PDF and XML format however is not published due to the journals' copy rights.
- `Survey` this folder contains the responses of the survey 87 survey participants as CSV file.

## Data Analysis Workflow (Source Code Overview)

- **Part 1**: Processing of Articles And Feature Extraction
    - **Pipeline Step 1**: Processing articles (in PDF or XML format, depending on journal), and creating Tables
    - **Pipeline Step 2**: Combination of journal specific tables to generate large master tables
    - **Pipeline Step 3**: Retrieval of Citation Counts From CrossRef API, and Word Counts (text lengths)
- **Part 2**: Creation of Complete Dataset
    - **Pipeline Step 4**: Combination of journal specific tables for text length to generate large master tables
    - **Pipeline Step 5**: Final large table generator
- **Part 3**: Analysis of Dataset
    - **Pipeline Step 6**: Analysis of Article Corpus (generating tables and figures)
    - **Pipeline Step 7**: Analysis of Survey Data (generating tables and figures)

For further details please review the exhaustive documentation in the single python scripts.

## Citations

If you find our work, insights or dataset interesting, please feel free to cite our work upon usage:
```
Kevin Riehl, Anastasios Kouvelas, Michalis Makridis.2024. Simulation study reproducibility - an inventory & recommendations for the field of transportation.  
```
