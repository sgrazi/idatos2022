import pandas as pd
import requests
from bs4 import BeautifulSoup

def query_new_id(name,ids):
    try:
        print(name)
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
        page = requests.get(
            "https://www.imdb.com/find?q="
            + name.replace(" ", "%20")
            + "&s=tt&ref_=fn_al_tt_mr"
            , headers=headers)
        soup = BeautifulSoup(page.text, "html.parser")
        
        id_arr = soup.find_all("a", {"class": "ipc-metadata-list-summary-item__t"})
        for id_element in id_arr:
            id = id_element.get("href").split("/")[2]
            if id not in ids:
                ids.append(id)
                return id
    except Exception as e:
        print(e)
        return ""

def correct_ids(path):
    df = pd.read_csv(path)
    ids = []
    for i, row in df.iterrows():
        if df.at[i,'id'] != "" and df.at[i,'id'] not in ids:
            ids.append(df.at[i,'id'])
        elif df.at[i,'id'] != "":
            df.at[i,'id'] = query_new_id(df.at[i,'title'],ids)
    
    return df

if __name__ == "__main__":
    # para preprocesar un dataset
    # df = correct_ids('../datasets/amazon_prime_titles_updatedIDs_poster.csv')
    # df.to_csv("../datasets/amazon_prime_titles_updatedIDs_poster2.csv", index=False)
    # df = correct_ids('../datasets/hbo_titles_updatedIDs_poster.csv')
    # df.to_csv("../datasets/hbo_titles_updatedIDs_poster2.csv", index=False)
    # df = correct_ids('../datasets/hulu_titles_updatedIDs_poster.csv')
    # df.to_csv("../datasets/hulu_titles_updatedIDs_poster2.csv", index=False)
    # df = correct_ids('../datasets/MoviesOnStreamingPlatforms_updatedIDs_poster.csv')
    # df.to_csv("../datasets/MoviesOnStreamingPlatforms_updatedIDs_poster2.csv", index=False)
    df = correct_ids('../datasets/netflix_titles_updatedIDs_poster.csv')
    df.to_csv("../datasets/netflix_titles_updatedIDs_poster2.csv", index=False)
