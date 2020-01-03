import pandas as pd
import numpy as np
from scipy import stats

def remove_outlier(df_in, col_name):
    df_out = df_in[np.abs(stats.zscore(df_in[col_name])) < 2.5]
    return df_out

def df_clean_merge(df1_orig, df2_orig, fyear):
    
    imdb_df = df1_orig.copy()
    metacritic_df = df2_orig.copy()

    imdb_df.drop(columns=['original_title', 'year', 'language', 'actors',
                          'description', 'avg_vote',
                          'votes', 'production_company'], inplace=True)
    new_column_list = ['imdb_id', 'title', 'release_date', 'genre', 'duration',
                       'country', 'director',
                       'writer', 'budget', 'domestic_income',
                       'worldwide_income', 'metascore',
                       'imdb_user_score', 'imdb_critic_score']
    imdb_df.columns = new_column_list
    imdb_df.release_date = pd.to_datetime(imdb_df.release_date)
    imdb_df.drop(imdb_df[imdb_df['release_date'].dt.year < fyear].index,
                 inplace=True)
    imdb_df.drop(imdb_df[imdb_df['country'] != 'USA'].index, inplace=True)
    imdb_df.drop(columns=['metascore', 'imdb_critic_score'], inplace=True)
    imdb_df.drop(columns=['country', 'writer'], inplace=True)
    imdb_df.dropna(subset=['budget'], inplace=True)
    imdb_df.dropna(subset=['domestic_income'], inplace=True)
    imdb_df.dropna(subset=['worldwide_income'], inplace=True)
    imdb_df.dropna(subset=['imdb_user_score'], inplace=True)
    metacritic_df.drop(columns=['release_date', 'genre', 'meta_mixed',
                                'meta_negative', 'meta_positive', 'metascore',
                                'user_mixed', 'user_negative', 'user_positive'],
                       inplace=True)
    metacritic_df.columns = ['title', 'metacritic_user_score']
    movies_df = pd.merge(imdb_df, metacritic_df, on='title', how='left')
    movies_df.drop_duplicates(subset='title', inplace=True)
    movies_df['metacritic_user_score'] = movies_df['metacritic_user_score'].replace('tbd', 'NaN', regex=True)
    movies_df.metacritic_user_score = movies_df.metacritic_user_score.astype(float)
    meta_mean = movies_df.metacritic_user_score.mean()
    movies_df.metacritic_user_score.fillna(value=meta_mean, inplace=True)
    movies_df['budget'] = movies_df['budget'].astype(str)
    movies_df['budget'] = movies_df['budget'].map(lambda x: x.split(' ')[1])
    movies_df['budget'] = movies_df['budget'].astype(float)
    movies_df['domestic_income'] = movies_df['domestic_income'].astype(str)
    movies_df['domestic_income'] = movies_df['domestic_income'].map(lambda x: x.split(' ')[1])
    movies_df['domestic_income'] = movies_df['domestic_income'].astype(float)
    movies_df['worldwide_income'] = movies_df['worldwide_income'].astype(str)
    movies_df['worldwide_income'] = movies_df['worldwide_income'].map(lambda x: x.split(' ')[1])
    movies_df['worldwide_income'] = movies_df['worldwide_income'].astype(float)
    movies_df = movies_df.join(movies_df.genre.str.get_dummies(', '))
    movies_df['domestic_roi'] = (movies_df['domestic_income']/movies_df['budget'])*100
    movies_df['worldwide_roi'] = (movies_df['worldwide_income']/movies_df['budget'])*100
    movies_df['domestic_profit_loss'] = movies_df['domestic_income']-movies_df['budget']
    movies_df['worldwide_profit_loss'] = movies_df['worldwide_income']-movies_df['budget']
    columns = ['budget', 'domestic_income', 'worldwide_income',\
           'domestic_profit_loss', 'worldwide_profit_loss']
    for column in columns:
        movies_df[column] = movies_df[column].map(lambda x: round(x/1000000, ndigits=1))
    movies_df['domestic_roi'] = movies_df['domestic_roi'].map(lambda x: int(round(x, ndigits=0)))
    movies_df['worldwide_roi'] = movies_df['worldwide_roi'].map(lambda x: int(round(x, ndigits=0)))
    
    return movies_df