import pandas as pd
import json
from country import generate_list_of_countries
from models.platform import Platform


def equalize_genres(genres1, genres2):
    genres1 = genres1.split(", ")
    for genre in genres1:
        if genre not in genres2:
            genres2 += ", " + genre

    return genres2


def generate_new_csv_hbo(path):
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
            countries = generate_list_of_countries(list_countries)

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


def generate_csv_for_api_movies():
    disneyplus = Platform.get_by_name("Disney+")
    if disneyplus is None:
        disneyplus = Platform()
        disneyplus.name = "Disney+"
        disneyplus.save()
    paramount = Platform.get_by_name("Paramount+")
    if paramount is None:
        paramount = Platform()
        paramount.name = "Paramount+"
        paramount.save()
    showtime = Platform.get_by_name("Showtime")
    if showtime is None:
        showtime = Platform()
        showtime.name = "Showtime"
        showtime.save()
    zee5 = Platform.get_by_name("ZEE5")
    if zee5 is None:
        zee5 = Platform()
        zee5.name = "ZEE5"
        zee5.save()
    peacock = Platform.get_by_name("Peacock")
    if peacock is None:
        peacock = Platform()
        peacock.name = "Peacock"
        peacock.save()
    starz = Platform.get_by_name("Starz")
    if starz is None:
        starz = Platform()
        starz.name = "Starz"
        starz.save()
    mubi = Platform.get_by_name("Mubi")
    if mubi is None:
        mubi = Platform()
        mubi.name = "Mubi"
        mubi.save()
    itunes = Platform.get_by_name("iTunes")
    if itunes is None:
        itunes = Platform()
        itunes.name = "iTunes"
        itunes.save()
    apple = Platform.get_by_name("AppleTV+")
    if apple is None:
        apple = Platform()
        apple.name = "AppleTV+"
        apple.save()

    stravdf = pd.read_csv("../datasets/strav_dataset.csv")
    stravdf.rename(columns={"tmdbID": "id"}, inplace=True)
    stravdf.drop(["overview"], axis=1, inplace=True)
    stravdf.drop(["originalLanguage"], axis=1, inplace=True)
    stravdf.drop(["year"], axis=1, inplace=True)

    tmdbdf = pd.read_csv("../datasets/tmdb_dataset.csv")
    tmdbdf.drop(["title"], axis=1, inplace=True)
    tmdbdf.drop(["vote_average"], axis=1, inplace=True)
    tmdbdf.drop(["popularity"], axis=1, inplace=True)

    df = pd.merge(stravdf, tmdbdf, on="id")

    # unnecessary column
    df.drop(["id"], axis=1, inplace=True)

    # compare genres on both datasets
    for i, row in df.iterrows():
        if df.at[i, "genres"] != df.at[i, "genre_ids"]:
            df.at[i, "genres"] = equalize_genres(
                df.at[i, "genres"], df.at[i, "genre_ids"]
            )

    df.drop(["genre_ids"], axis=1, inplace=True)

    for i, row in df.iterrows():

        list_of_countries = json.loads(df.at[i, "countries"].replace("'", '"'))
        df.at[i, "countries"] = generate_list_of_countries(list_of_countries)

    for i, row in df.iterrows():
        if not pd.isna(df.at[i, "release_date"]):
            df.at[i, "release_year"] = df.at[i, "release_date"].split("-")[0]

    # now integrate utelly

    utellydf = pd.read_csv("../datasets/utelly_dataset.csv")
    utellydf.drop(["name"], axis=1, inplace=True)

    df.rename(columns={"imdbID": "id"}, inplace=True)
    df = pd.merge(df, utellydf, on="id")

    # iterate, unify streaming services and rating
    for i, row in df.iterrows():
        if df.at[i, "streamingInfo.disney.us.added"] > 0:
            if "Disney+" not in str(df.at[i, "streaming_services"]):
                df.at[i, "streaming_services"] = (
                    str(df.at[i, "streaming_services"]) + ", Disney+"
                )
        if df.at[i, "streamingInfo.paramount.us.added"] > 0:
            if "Paramount+" not in str(df.at[i, "streaming_services"]):
                df.at[i, "streaming_services"] = (
                    str(df.at[i, "streaming_services"]) + ", Paramount+"
                )
        if df.at[i, "streamingInfo.showtime.us.added"] > 0:
            if "Showtime" not in str(df.at[i, "streaming_services"]):
                df.at[i, "streaming_services"] = (
                    str(df.at[i, "streaming_services"]) + ", Showtime"
                )
        if df.at[i, "streamingInfo.hulu.us.added"] > 0:
            if "Hulu" not in str(df.at[i, "streaming_services"]):
                df.at[i, "streaming_services"] = (
                    str(df.at[i, "streaming_services"]) + ", Hulu"
                )
        if df.at[i, "streamingInfo.hulu.us.added"] > 0:
            if "Netflix" not in str(df.at[i, "streaming_services"]):
                df.at[i, "streaming_services"] = (
                    str(df.at[i, "streaming_services"]) + ", Netflix"
                )
        if df.at[i, "streamingInfo.prime.us.added"] > 0:
            if "Amazon Prime Video" not in str(df.at[i, "streaming_services"]):
                df.at[i, "streaming_services"] = (
                    str(df.at[i, "streaming_services"]) + ", Amazon Prime Video"
                )
        if df.at[i, "streamingInfo.hbo.us.added"] > 0:
            if "HBO Max" not in str(df.at[i, "streaming_services"]):
                df.at[i, "streaming_services"] = (
                    str(df.at[i, "streaming_services"]) + ", HBO Max"
                )
        if df.at[i, "streamingInfo.zee5.us.added"] > 0:
            if "ZEE5" not in str(df.at[i, "streaming_services"]):
                df.at[i, "streaming_services"] = (
                    str(df.at[i, "streaming_services"]) + ", ZEE5"
                )
        if df.at[i, "streamingInfo.peacock.us.added"] > 0:
            if "Peacock" not in str(df.at[i, "streaming_services"]):
                df.at[i, "streaming_services"] = (
                    str(df.at[i, "streaming_services"]) + ", Peacock"
                )
        if df.at[i, "streamingInfo.starz.us.added"] > 0:
            if "Starz" not in str(df.at[i, "streaming_services"]):
                df.at[i, "streaming_services"] = (
                    str(df.at[i, "streaming_services"]) + ", Starz"
                )
        if df.at[i, "streamingInfo.mubi.us.added"] > 0:
            if "Starz" not in str(df.at[i, "streaming_services"]):
                df.at[i, "streaming_services"] = (
                    str(df.at[i, "streaming_services"]) + ", Mubi"
                )
        if df.at[i, "streamingInfo.apple.us.added"] > 0:
            if "AppleTV+" not in str(df.at[i, "streaming_services"]):
                df.at[i, "streaming_services"] = (
                    str(df.at[i, "streaming_services"]) + ", AppleTV+"
                )
        df.at[i, "imdbRating"] = (df.at[i, "imdbRating"] + df.at[i, "tmdbRating"]) / 2

    df.drop(["streamingInfo.disney.us.added"], axis=1, inplace=True)
    df.drop(["streamingInfo.paramount.us.added"], axis=1, inplace=True)
    df.drop(["streamingInfo.showtime.us.added"], axis=1, inplace=True)
    df.drop(["streamingInfo.hulu.us.added"], axis=1, inplace=True)
    df.drop(["streamingInfo.netflix.us.added"], axis=1, inplace=True)
    df.drop(["streamingInfo.prime.us.added"], axis=1, inplace=True)
    df.drop(["streamingInfo.hbo.us.added"], axis=1, inplace=True)
    df.drop(["streamingInfo.zee5.us.added"], axis=1, inplace=True)
    df.drop(["streamingInfo.peacock.us.added"], axis=1, inplace=True)
    df.drop(["streamingInfo.starz.us.added"], axis=1, inplace=True)
    df.drop(["streamingInfo.mubi.us.added"], axis=1, inplace=True)
    df.drop(["streamingInfo.apple.us.added"], axis=1, inplace=True)

    df.drop(["streamingInfo.disney.us.leaving"], axis=1, inplace=True)
    df.drop(["streamingInfo.paramount.us.leaving"], axis=1, inplace=True)
    df.drop(["streamingInfo.showtime.us.leaving"], axis=1, inplace=True)
    df.drop(["streamingInfo.hulu.us.leaving"], axis=1, inplace=True)
    df.drop(["streamingInfo.netflix.us.leaving"], axis=1, inplace=True)
    df.drop(["streamingInfo.prime.us.leaving"], axis=1, inplace=True)
    df.drop(["streamingInfo.hbo.us.leaving"], axis=1, inplace=True)
    df.drop(["streamingInfo.zee5.us.leaving"], axis=1, inplace=True)
    df.drop(["streamingInfo.peacock.us.leaving"], axis=1, inplace=True)
    df.drop(["streamingInfo.starz.us.leaving"], axis=1, inplace=True)
    df.drop(["streamingInfo.mubi.us.leaving"], axis=1, inplace=True)
    df.drop(["streamingInfo.apple.us.leaving"], axis=1, inplace=True)
    df.drop(["release_date"], axis=1, inplace=True)

    df.rename(columns={"posterURLs.original": "poster"}, inplace=True)
    df.drop(["tmdbRating"], axis=1, inplace=True)
    df.rename(columns={"imdbRating": "rating"}, inplace=True)

    df.to_csv("../datasets/api_titles_updatedIDs_poster.csv", index=False)
    return df


if __name__ == "__main__":
    # path = "../datasets/hbo-max-tv-shows-and-movies/titles.csv"
    # generate_new_csv_hbo(path)
    generate_csv_for_api_movies()
