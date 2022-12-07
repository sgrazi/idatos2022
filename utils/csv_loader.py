import json
from datetime import datetime

import pandas as pd
from genre_mapper import GENRE_MAPPER
from models.genre import Genre
from models.movie import Movie
from models.platform import Platform


def load_csv(path):
    return pd.read_csv(path)


def insert_genres(genres):
    list_of_genres = []
    for genre in genres:
        genre_name = genre.upper()
        if genre_name in GENRE_MAPPER:
            genre_name = GENRE_MAPPER[genre_name]

        g = Genre.get_by_name(genre_name)
        if g is None:
            g = Genre()
            g.name = genre_name
            g.save()

        filtered = list(filter(lambda x: x.id == g.id, list_of_genres))
        if len(filtered) == 0:
            list_of_genres.append(g)

    return list_of_genres


def load_movies(df, platform):
    new_movies = 0
    updated_movies = 0
    duplicated_ids = 0
    for index, row in df.iterrows():
        try:
            if not pd.isna(row["id"]):

                genres = []
                if not pd.isna(row["listed_in"]):
                    genres = insert_genres(row["listed_in"].split(", "))

                movie = Movie.get_by_id(row["id"])

                if movie is None:
                    movie = Movie(
                        id=row["id"],
                        title=row["title"],
                        country=row["country"],
                        release_year=row["release_year"],
                        duration=row["duration"],
                        description=row["description"],
                        image=row["poster"],
                    )
                    movie.save([platform], genres)
                    new_movies += 1
                else:
                    movie.update([platform], genres)
                    updated_movies += 1
        except Exception as e:
            duplicated_ids += 1
            print(e)
            print("Error adding movie: " + row["title"])

    print("New movies: " + str(new_movies))
    print("Updated movies: " + str(updated_movies))
    print("Duplicated ids: " + str(duplicated_ids))


def load_amazon_csv(path):
    df = load_csv(path)
    amazon = Platform.get_by_name("Amazon Prime Video")

    if amazon is None:
        amazon = Platform()
        amazon.name = "Amazon Prime Video"
        amazon.save()

    df = df.query('type == "Movie"')
    load_movies(df, amazon)


def load_netflix_csv(path):
    df = load_csv(path)
    netflix = Platform.get_by_name("Netflix")

    if netflix is None:
        netflix = Platform()
        netflix.name = "Netflix"
        netflix.save()

    df = df.query('type == "Movie"')
    load_movies(df, netflix)


def load_hulu_csv(path):
    df = load_csv(path)
    hulu = Platform.get_by_name("Hulu")

    if hulu is None:
        hulu = Platform()
        hulu.name = "Hulu"
        hulu.save()

    df = df.query('type == "Movie"')
    load_movies(df, hulu)


def load_hbo_max_csv(path):
    df = load_csv(path)
    hbo_max = Platform.get_by_name("HBO Max")

    if hbo_max is None:
        hbo_max = Platform()
        hbo_max.name = "HBO Max"
        hbo_max.save()

    df = df.query('type == "Movie"')
    load_movies(df, hbo_max)


def load_api_movies(path):
    df = load_csv(path)
    new_movies = 0
    updated_movies = 0
    for i, row in df.iterrows():
        try:
            genres = []
            if not pd.isna(row["genres"]):
                genres = insert_genres(row["genres"].split(", "))

            platforms = []
            if not pd.isna(row["streaming_services"]):
                for platform_name in row["streaming_services"].split(", "):
                    platform = Platform.get_by_name(platform_name)
                    if platform is not None:
                        platforms.append(platform)

            movie = Movie.get_by_id(row["id"])

            if movie is None:
                movie = Movie(
                    id=row["id"],
                    title=row["title"],
                    country=row["countries"],  # es un string de lista? formatear
                    release_year=row["release_year"],
                    duration=row["runtime"],
                    description=row["overview"],
                    image=row["poster"],
                )
                new_movies += 1
                movie.save(platforms, genres)
            else:
                updated_movies += 1
                movie.update(platforms, genres)
        except Exception as e:
            print(e)
            print("Error adding movie: " + row["title"])

    print("New movies: " + str(new_movies))
    print("Updated movies: " + str(updated_movies))


def load_movies_on_streaming_platforms(path):
    df = load_csv(path)
    new_movies = 0
    updated_movies = 0
    netflix = Platform.get_by_name("Netflix")
    if not netflix:
        netflix = Platform()
        netflix.name = "Netflix"
        netflix.save()

    amazon = Platform.get_by_name("Amazon Prime Video")
    if not amazon:
        amazon = Platform()
        amazon.name = "Amazon Prime Video"
        amazon.save()

    hulu = Platform.get_by_name("Hulu")
    if not hulu:
        hulu = Platform()
        hulu.name = "Hulu"
        hulu.save()
    disney = Platform.get_by_name("Disney+")
    if not disney:
        disney = Platform()
        disney.name = "Disney+"
        disney.save()

    for i, row in df.iterrows():

        if pd.isna(row["id"]):
            continue
        list_of_platforms = []
        if row["Netflix"] == 1:
            list_of_platforms.append(netflix)

        if row["Prime Video"] == 1:
            list_of_platforms.append(amazon)

        if row["Hulu"] == 1:
            list_of_platforms.append(hulu)

        if row["Disney+"] == 1:
            list_of_platforms.append(disney)

        movie = Movie.get_by_id(row["id"])
        if movie is None:
            movie = Movie(
                id=row["id"],
                title=row["title"],
                image=row["poster"],
                release_year=row["Year"],
            )
            new_movies += 1
            movie.save(platforms=list_of_platforms, genres=[])
        else:
            updated_movies += 1
            movie.update(platforms=list_of_platforms, genres=[])

    print("New movies: " + str(new_movies))
    print("Updated movies: " + str(updated_movies))


if __name__ == "__main__":
    time1 = datetime.now()
    load_amazon_csv("../datasets/amazon_prime_titles_updatedIDs_poster.csv")
    print("Amazon Prime Video: " + str(datetime.now() - time1))
    time = datetime.now()
    load_netflix_csv("../datasets/netflix_titles_updatedIDs_poster.csv")
    print("Netflix: " + str(datetime.now() - time))
    time = datetime.now()
    load_hulu_csv("../datasets/hulu_titles_updatedIDs_poster.csv")
    print("Hulu: " + str(datetime.now() - time))
    time = datetime.now()
    load_hbo_max_csv("../datasets/hbo_titles_updatedIDs_poster.csv")
    print("HBO Max: " + str(datetime.now() - time))
    time = datetime.now()
    load_api_movies("../datasets/api_titles_updatedIDs_poster.csv")
    print("APIs: " + str(datetime.now() - time))
    time = datetime.now()
    load_movies_on_streaming_platforms(
        "../datasets/MoviesOnStreamingPlatforms_updatedIDs_poster.csv"
    )
    print("MoviesOnStreamingPlatforms: " + str(datetime.now() - time))
    print("TIEMPO TOTAL:" + str(time1 - datetime.now()))
    pass
