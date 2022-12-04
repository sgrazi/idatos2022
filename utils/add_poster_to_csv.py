import pandas as pd
import requests
from bs4 import BeautifulSoup


def query_id(movieid):
    try:
        print(movieid)
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36"
        }
        movie_page = requests.get(
            "http://www.imdb.com/title/" + movieid, headers=headers
        )
        soup = BeautifulSoup(movie_page.text, "html.parser")
        mediaviewer = soup.find("a", {"class": "ipc-lockup-overlay ipc-focusable"}).get(
            "href"
        )
        poster_page = requests.get(
            "https://www.imdb.com" + mediaviewer, headers=headers
        )
        soup = BeautifulSoup(poster_page.text, "html.parser")
        images = soup.findAll("img")
        return images[1].get("src")
    except Exception as e:
        print(e)
        return ""


def load_csv_and_fill_ids(path):
    # demora, mucho
    df = pd.read_csv(path)
    if path == "../datasets/amazon_prime_titles_updatedIDs.csv":
        for i, row in df.iterrows():
            id = query_id(df.at[i,'id'])
            df.at[i,'poster'] = id
    elif path == "../datasets/hbo_titles_updatedIDs.csv":
        for i, row in df.iterrows():
            id = query_id(df.at[i, "show_id"])
            df.at[i, "poster"] = id
    elif path == "../datasets/hulu_titles_updatedIDs.csv":
        for i, row in df.iterrows():
            id = query_id(df.at[i, "id"])
            df.at[i, "poster"] = id
    elif path == "../datasets/MoviesOnStreamingPlatforms_updatedIDs.csv":
        for i, row in df.iterrows():
            id = query_id(df.at[i, "id"])
            df.at[i, "poster"] = id
    elif path == "../datasets/netflix_titles_updatedIDs.csv":
        for i, row in df.iterrows():
            id = query_id(df.at[i,'id'])
            df.at[i,'poster'] = id
    elif path == "../datasets/utelly_dataset.csv":
        for i, row in df.iterrows():
            id = query_id(df.at[i,'id'])
            df.at[i,'poster'] = id
    return df


if __name__ == "__main__":
    # para preprocesar un dataset
    df = load_csv_and_fill_ids('../datasets/utelly_dataset.csv')
    df.to_csv("../datasets/utelly_dataset_poster.csv", index=False)
