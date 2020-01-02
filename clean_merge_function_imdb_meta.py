import pandas as pd
import numpy as np

def remove_outlier(df_in, col_name):
    q1 = df_in[col_name].quantile(0.25)
    q3 = df_in[col_name].quantile(0.75)
    iqr = q3-q1 #Interquartile range
    fence_low  = q1-1.5*iqr
    fence_high = q3+1.5*iqr
    df_out = df_in.loc[(df_in[col_name] > fence_low) & (df_in[col_name] < fence_high)]
    return df_out

def genre_binary(genre, list_of_genres):
    value = None
    if genre in list_of_genres:
        value = 1
    else:
        value = 0
    return value

def df_clean_merge(df1_orig, df2_orig):
    
    df1 = df1_orig
    df2 = df2_orig
    df3 = pd.DataFrame()

    # Dropping columns that won't be used.
    df1.drop(columns=['original_title', 'year', 'language', 'actors', 'description', 'avg_vote',\
                          'votes', 'production_company'], inplace=True)

    # Renaming and simplifying column names to be more descriptive.
    new_column_list = ['imdb_id', 'title', 'release_date', 'genre', 'duration', 'country', 'director',\
                       'writer', 'budget', 'domestic_income', 'worldwide_income', 'metascore',\
                       'imdb_user_score', 'imdb_critic_score']
    df1.columns = new_column_list
    
    # Convert release date to datetime object. If date only contains year, defaulting to January 1st.
    df1.release_date = pd.to_datetime(df1.release_date)

    # Filter out movies without a release date and made before 2000.
    df1.drop(df1[df1['release_date'].dt.year < 2000].index, inplace=True)

    # Filter out movies made outside the USA.
    df1.drop(df1[df1['country'] != 'USA'].index, inplace=True)
    
    # Drop country, director, and writer columns.
    df1.drop(columns=['country', 'director', 'writer'], inplace=True)

    # Filter out null values for budget and domestic_income.
    df1.dropna(subset=['budget'], inplace=True)
    df1.dropna(subset=['domestic_income'], inplace=True)
    
    # Drop critic ratings due to assumption that it is not valuable.
    df1 = df1.drop(columns=['metascore', 'imdb_critic_score'])

    # Filter out 5 entries without an imdb user score.
    df1.dropna(subset=['imdb_user_score'], inplace=True)
    
    # Drop unused columns from metacritic file
    df2.drop(columns=['release_date', 'genre', 'meta_mixed', 'meta_negative', 'meta_positive', 'metascore',\
                               'user_mixed', 'user_negative', 'user_positive'], inplace=True)

    # Rename columns to align with imdb_df.
    df2.columns = ['title', 'metacritic_user_score']
    
    # Merge metacritic userscore into movies_df based on titles
    df3 = pd.merge(df1, df2, left_on='title', right_on='title', how='left')
    
    # Drop duplicate entries based on title
    df3.drop_duplicates(subset='title', inplace=True)
    
    # Replace 'tbd' metacritic user scores with 'NaN'
    df3['metacritic_user_score'] = df3['metacritic_user_score'].replace('tbd', 'NaN', regex=True)

    # Convert series dtype to float.
    df3.metacritic_user_score = df3.metacritic_user_score.astype(float)
    
    # Replace null values with mean score.
    meta_mean = df3.metacritic_user_score.mean()
    df3.metacritic_user_score.fillna(value=meta_mean, inplace=True)

    # Format budget, domestic, and worldwide boxoffice columns and delete dollar sign and extra space.
    df3['budget'] = df3['budget'].astype(str)
    df3['budget'] = df3['budget'].map(lambda x: x.split(' ')[1])

    df3['domestic_income'] = df3['domestic_income'].astype(str)
    df3['domestic_income'] = df3['domestic_income'].map(lambda x: x.split(' ')[1])

    df3['worldwide_income'] = df3['worldwide_income'].astype(str)
    df3['worldwide_income'] = df3['worldwide_income'].map(lambda x: x.split(' ')[1])
    
    # Convert budget, domestic, and worldwide columns into floats.
    df3['budget'] = df3['budget'].astype(float)
    df3['domestic_income'] = df3['domestic_income'].astype(float)
    df3['worldwide_income'] = df3['worldwide_income'].astype(float)
    
    unique_genres = set([x for genre in [genres.split(', ') for genres in df3['genre']] for x in genre])
    
    for genre in unique_genres:
        df3[genre] = df3['genre'].map(lambda x: genre_binary(genre, x))
    
    # Create ROI and profit/loss columns for both domestic & worldwide boxoffice.
    df3['domestic_roi'] = (df3['domestic_income']/df3['budget'])*100
    df3['worldwide_roi'] = (df3['worldwide_income']/df3['budget'])*100
    df3['domestic_profit_loss'] = df3['domestic_income']-df3['budget']
    df3['worldwide_profit_loss'] = df3['worldwide_income']-df3['budget']
    
    return df3