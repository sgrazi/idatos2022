import os, glob, json
import pandas as pd
from pathlib import Path

genres = {
    28: "Action",
    12: "Adventure",
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
jsons_paths = os.path.join("../../data/strav-jsons/", "*.json")
csv_path = Path("../../datasets/strav_dataset.csv")
json_list = glob.glob(jsons_paths)
for json_file in json_list:
    f = open(json_file)
    json_data = json.load(f)
    f.close()
    data = pd.json_normalize(json_data)
    dfs.append(data)

df = pd.concat(dfs, ignore_index=True)
df.drop(["imdbVoteCount"], axis=1, inplace=True)
df.drop(["backdropPath"], axis=1, inplace=True)
df.drop(["backdropURLs.300"], axis=1, inplace=True)
df.drop(["backdropURLs.780"], axis=1, inplace=True)
df.drop(["backdropURLs.1280"], axis=1, inplace=True)
df.drop(["backdropURLs.original"], axis=1, inplace=True)
df.drop(["originalTitle"], axis=1, inplace=True)
df.drop(["cast"], axis=1, inplace=True)
df.drop(["significants"], axis=1, inplace=True)
df.drop(["tagline"], axis=1, inplace=True)
df.drop(["video"], axis=1, inplace=True)
df.drop(["posterPath"], axis=1, inplace=True)
df.drop(["posterURLs.92"], axis=1, inplace=True)
df.drop(["posterURLs.154"], axis=1, inplace=True)
df.drop(["posterURLs.185"], axis=1, inplace=True)
df.drop(["posterURLs.342"], axis=1, inplace=True)
df.drop(["posterURLs.500"], axis=1, inplace=True)
df.drop(["posterURLs.780"], axis=1, inplace=True)
df.drop(["age"], axis=1, inplace=True)
df.drop(["streamingInfo.disney.us.link"], axis=1, inplace=True)
df.drop(["streamingInfo.paramount.us.link"], axis=1, inplace=True)
df.drop(["streamingInfo.showtime.us.link"], axis=1, inplace=True)
df.drop(["streamingInfo.hulu.us.link"], axis=1, inplace=True)
df.drop(["streamingInfo.netflix.us.link"], axis=1, inplace=True)
df.drop(["streamingInfo.prime.us.link"], axis=1, inplace=True)
df.drop(["streamingInfo.hbo.us.link"], axis=1, inplace=True)
df.drop(["streamingInfo.zee5.us.link"], axis=1, inplace=True)
df.drop(["streamingInfo.peacock.us.link"], axis=1, inplace=True)
df.drop(["streamingInfo.starz.us.link"], axis=1, inplace=True)
df.drop(["streamingInfo.mubi.us.link"], axis=1, inplace=True)
df.drop(["streamingInfo.apple.us.link"], axis=1, inplace=True)
j = df.columns.get_loc("genres")
for i, row in df.iterrows():
    res = str(df.iat[i, j])
    for id, genre in genres.items():
        res = res.replace(str(id), genre)
    res = res[1:-1]
    df.iat[i, j] = res
df.to_csv(csv_path, index=False)
