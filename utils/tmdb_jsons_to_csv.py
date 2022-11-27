import os, glob, json
import pandas as pd
from pathlib import Path

genres = {
    28: "Action",
    12:  "Adventure",
    16: "Animation",
    35: "Comedy",          
    80: "Crime",         
    99: "Documentary",     
    18: "Drama",              
    10751: "Family",          
    14: "Fantasy",         
    36: "History",       
    27: "Horror",          
    10402: "Music",           
    9648: "Mystery",       
    10749: "Romance",         
    878: "Science Fiction", 
    10770: "TV Movie",        
    53: "Thriller",        
    10752: "War",             
    37: "Western",         
}

dfs = []
jsons_paths = os.path.join("../tmdb-jsons/", "*.json")
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
    dfs.append(data)
df = pd.concat(dfs, ignore_index=True)
j = df.columns.get_loc('genre_ids')
for i, row in df.iterrows():
    res = str(df.iat[i, j])
    for id, genre in genres.items():
        res = res.replace(str(id), genre)
    res = res[1:-1] 
    df.iat[i, j] = res
df.to_csv(csv_path, index=False)
