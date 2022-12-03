import pandas as pd
from genre_mapper import GENRE_MAPPER
from models.genre import Genre
from models.movie import Movie
from models.platform import Platform
from datetime import datetime


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
    for index, row in df.iterrows():
        try:
            genres = []
            if not pd.isna(row["listed_in"]):
                genres = insert_genres(row["listed_in"].split(", "))

            movie = Movie.get_by_title(row["title"])

            if movie is None:
                movie = Movie(
                    title=row["title"],
                    country=row["country"],
                    release_year=row["release_year"],
                    duration=row["duration"],
                    description=row["description"],
                )
                new_movies += 1
                movie.save([platform], genres)
            else:
                updated_movies += 1
                movie.update([platform], genres)
        except Exception as e:
            print(e)
            print("Error adding movie: " + row["title"])
        # if index >= 100:
        #     break

    print("New movies: " + str(new_movies))
    print("Updated movies: " + str(updated_movies))


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


# def load_utelly_movies(df): # WIP
#     db = SingletonDatabase.get_instance()
#     movie_df = df.drop(["streaming_service"], axis=1)
#     movie_df.drop_duplicates(inplace=True)
#     for index, row in movie_df.iterrows():
#         movie = Movie()
#         movie.id = row['id']
#         movie.title = row['name']
#         try:
#             db.session.add(movie)
#             db.session.commit()
#         except Exception as e:
#             print(e)
#             db.session.rollback()
#             print(f"Error al crear el usuario {row['id']}")

if __name__ == "__main__":
    time = datetime.now()
    load_amazon_csv("../datasets/amazon_prime_titles.csv")
    print("Amazon Prime Video: " + str(datetime.now() - time))
    time = datetime.now()
    load_netflix_csv("../datasets/netflix_titles.csv")
    print("Netflix: " + str(datetime.now() - time))
    time = datetime.now()
    load_hulu_csv("../datasets/hulu_titles.csv")
    print("Hulu: " + str(datetime.now() - time))
    time = datetime.now()
    load_hbo_max_csv("../datasets/hbo_titles.csv")
    print("HBO Max: " + str(datetime.now() - time))
