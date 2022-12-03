import os, glob, json
import pandas as pd
from pathlib import Path

dfs = []
jsons_paths = os.path.join("../utelly-jsons/", "*.json")
csv_path = Path("../datasets/utelly_dataset.csv")
json_list = glob.glob(jsons_paths)
for json_file in json_list:
    f = open(json_file)
    json_data = json.load(f)
    f.close()
    data = pd.json_normalize(json_data, max_level=2)
    data.drop(["variant"], axis=1, inplace=True)
    data.drop(["status_code"], axis=1, inplace=True)
    data.drop(["type"], axis=1, inplace=True)
    # reemplazamos collection.locations por los servicios
    if "collection.locations" in data.columns:
        # removemos columnas basura
        data.drop(["collection.weight"], axis=1, inplace=True)
        data.drop(["collection.picture"], axis=1, inplace=True)
        data.drop(["collection.source_ids.imdb"], axis=1, inplace=True)
        data.drop(["collection.id"], axis=1, inplace=True)
        # si esta en streaming, guardamos los servicios
        locations = pd.DataFrame.from_records(data["collection.locations"].values[0])
        locations.drop(["url"], axis=1, inplace=True)
        locations.drop(["icon"], axis=1, inplace=True)
        locations.drop(["id"], axis=1, inplace=True)
        locations.drop(["name"], axis=1, inplace=True)
        services = locations["display_name"].tolist()
        data["streaming_services"] = ", ".join(services)
    else:
        # si no existe la columna, se crea con valores vacios
        data["collection.locations"] = ""
    data.drop(["collection.locations"], axis=1, inplace=True)
    dfs.append(data)

df = pd.concat(dfs, ignore_index=True)
df.rename(columns={"collection.name": "name"}, inplace=True)
df.to_csv(csv_path, index=False)
