import os, glob, json
import pandas as pd
from pathlib import Path

dfs = []
jsons_paths = os.path.join("../tmdb-jsons/","*.json")
csv_path = Path("../datasets/tmdb_dataset.csv")
json_list = glob.glob(jsons_paths)
for json_file in json_list:
    f = open(json_file)
    json_data = json.load(f)
    f.close()
    data = pd.json_normalize(json_data["movie_results"])
    data.drop(["backdrop_path"], axis=1, inplace=True)
    data.drop(["adult"], axis=1, inplace=True)
    data.drop(["original_title"], axis=1, inplace=True)
    data.drop(["video"], axis=1, inplace=True)
    data.drop(["vote_count"], axis=1, inplace=True)
    data.drop(["poster_path"], axis=1, inplace=True)
    data.drop(["media_type"], axis=1, inplace=True)
    # expandimos los generos
    genres = pd.DataFrame(data["genre_ids"].values[0], columns=["genre_ids"])
    data.drop(["genre_ids"], axis=1, inplace=True)
    row = data
    # uso concat (merge no me funciona), tengo que tener misma cant de tuplas en ambos dataframes
    for x in range(0,genres.shape[0]-1):
        data = pd.concat([data,row],axis=0)
    data.reset_index(drop=True, inplace=True)
    data = pd.concat([data,genres],axis=1)
    dfs.append(data)

df = pd.concat(dfs, ignore_index=True)
df.to_csv(csv_path, index=False)