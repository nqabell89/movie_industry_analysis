# General Tasks

* forumulate questions
    * Which movie genres are most profitable?
    * Does higher budget equate to higher ratings?
    * Does higher ratings equate to higher profit/gross income?
    * Should we make movies shorter or longer? Are longer movies rated higher? More profitable?
    * Which studios should we partner with based on their success?
    * Over time, which genres have increased in popularity, rating, and profit?
    * ROI - output=optompize duration, genre, 
    * deck = 1-2 data cleaning slizes, 4 visualizations, how will i tell the story in 8-10 slides
    * how much data did I start with? how much did I have after finishing cleaning? 7-8 
    * * what aggragtes, transformations did I use? ex: combining audience scores
    * problem (slide 1) -> cleaning (slide 2-3) -> analysis/visualizations (slides )
* new data sets to create
    * movie length category (short, medium, long)
    * average profit per genre
* deliverables
    * README - Nick
    * Technical Notebook - Nick/Yasser
    * Non-Technical Notebook - OPTIONAL
    * Slidedeck Presentation - Nick
* data cleaning needs
    * Need to standardize columns across datasets in order to merge them
    * * example: movie title, name, title, etc
    * genre category is a mess; multiple duplicate entries with different genre tags
    * * also need to seperate multi-tagged strings by comma to create multiple columns with one genre each
    * need to remove duplicates, but first need to understand which duplicate entry is best to keep
    * need to remove replace null values and mistake values
    * * example: gross box office = 0
    * need to remove dollar signs from income/budget lines to convert to int
* visualizations
    * check for outliers with boxplots
    * check for corellations
* notes
    * reference week 2 day 3 for how to create .py script