import pandas as pd
import requests
from bs4 import BeautifulSoup

def query_id(name):
    try:
        print(name)
        page = requests.get('https://www.imdb.com/find?q='+name.replace(' ','%20')+'&s=tt&ref_=fn_al_tt_mr')
        soup = BeautifulSoup(page.text, 'html.parser')
        return soup.find('a', {'class': 'ipc-metadata-list-summary-item__t'}).get('href').split('/')[2]
    except:
        return ""

def load_csv_and_fill_ids(path):
    # demora, mucho
    df = pd.read_csv(path)
    if path == "../datasets/amazon_prime_titles.csv":
        df = df.query('type == "Movie"')
        for i, row in df.iterrows():
            id = query_id(df.at[i,'title'])
            df.at[i,'show_id'] = id
        df.rename(columns = {'show_id':'id'}, inplace = True)
    elif path == "../datasets/hulu_titles.csv":
        df = df.query('type == "Movie"')
        for i, row in df.iterrows():
            id = query_id(df.at[i,'title'])
            df.at[i,'show_id'] = id
        df.rename(columns = {'show_id':'id'}, inplace = True)
    elif path == "../datasets/MoviesOnStreamingPlatforms.csv":
        for i, row in df.iterrows():
            id = query_id(df.at[i,'Title'])
            df.at[i,'ID'] = id
        df.rename(columns = {'ID':'id'}, inplace = True)
    elif path == "../datasets/netflix_titles.csv":
        df = df.query('type == "Movie"')
        for i, row in df.iterrows():
            id = query_id(df.at[i,'title'])
            df.at[i,'show_id'] = id
        df.rename(columns = {'show_id':'id'}, inplace = True)
    return df

if __name__ == '__main__':
    # para preprocesar un dataset
    df = load_csv_and_fill_ids('../datasets/MoviesOnStreamingPlatforms.csv')
    df.to_csv("../datasets/MoviesOnStreamingPlatforms_updatedIDs.csv", index=False)