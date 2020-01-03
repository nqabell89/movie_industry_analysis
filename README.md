# movie_industry_analysis
This repository contains materials for the analysis of the movie industry. In a hypothetical project for Microsoft, I recommend an optimal movie profile for a possible market entrance into the movie making business. 

Author - Nicholas Abell

## Deliverables
    * Movie_Industry_EDA.ipynb - Technical Notebook/White Paper
    * Movie Industry Market Analysis.pptx - Slidedeck Presentation
    * Data_Wrangling.ipynb - Data wrangling notebook
    * clean_merge_function_imdb_meta.py - Python module for cleaning and merging data.
## Questions
    * Which movie genres are most profitable?
    * Which movie genres are rated higher by audiences?
    * What is average budget of movies in the most profitable genre?
    * What is the average runtime of movies in the most profitable genre?
    * Which directors have the most experience, success, and audience ratings in the most profitable genre?
    * Which release month would maximize box office performance?
## Assumptions
    * Popular movie trends have changed dramatically over time, and only movies released since 1990 should be analyzed for today's audiences.
    * Microsoft wants to create it's first movie in the US for a primarily domestic audience, while maximizing worldwide box office as a secondary goal.
    * In recent years, critic scores have become irrelevant for estimating the financial success and/or audience ratings of a film, and therefore are not useful in this analysis.
    * Microsoft wants to maxamize profitability and popularity for their first major film project, and is not limited by budget.
## Data Cleaning Considerations
    * need to standardize columns across datasets in order to merge them
    * * example: movie title, name, title, etc
    * genre category is a mess; multiple duplicate entries with different genre tags
    * * also need to seperate multi-tagged strings by comma to create multiple columns with one genre each
    * need to remove duplicates, but first need to understand which duplicate entry is best to keep
    * need to remove replace null values and mistake values
    * * example: gross box office = 0
    * need to remove dollar signs from income/budget lines to convert to int
    * need to convert dollar value columns into millions
    * need to create profit/loss and ROI columns for both domestic and worldwide box office