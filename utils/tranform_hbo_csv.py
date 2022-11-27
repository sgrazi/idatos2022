import pandas as pd
import pycountry
import json


def generate_new_csv(path):
    df = pd.read_csv(path)
    new_df = {
        "show_id": [],
        "type": [],
        "title": [],
        "country": [],
        "release_year": [],
        "duration": [],
        "listed_in": [],
        "description": [],
    }
    for index, row in df.iterrows():
        if row["type"] == "MOVIE":
            new_df["show_id"].append(row["id"])
            new_df["type"].append("Movie")
            new_df["title"].append(row["title"])
            countries = ""
            # for with index to get the last country
            list_countries = json.loads(row["production_countries"].replace("'", '"'))
            print(list_countries)

            for index, country_alpha_code in enumerate(list_countries):
                try:
                    print(index, country_alpha_code)
                    country = pycountry.countries.get(alpha_2=country_alpha_code).name
                    if index == len(list_countries) - 1:
                        countries += country
                    else:
                        countries += country + ", "
                except:
                    pass

            new_df["country"].append(countries)
            new_df["release_year"].append(row["release_year"])
            new_df["duration"].append(
                f"""{row["runtime"]} min""" if row["runtime"] else None
            )
            listed_in = ""
            list_of_genres = json.loads(row["genres"].replace("'", '"'))
            for index, genre in enumerate(list_of_genres):
                if index == len(list_of_genres) - 1:
                    listed_in += genre
                else:
                    listed_in += genre + ", "
            new_df["listed_in"].append(listed_in)
            new_df["description"].append(row["description"])
    new_df = pd.DataFrame(new_df)
    new_df.to_csv("../datasets/hbo_titles.csv", index=False)
    return new_df


if __name__ == "__main__":
    path = "../datasets/hbo-max-tv-shows-and-movies/titles.csv"
    generate_new_csv(path)
