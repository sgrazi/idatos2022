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

def equalize_genres(genres1, genres2):
    genres1 = genres1.split(", ")
    for genre in genres1:
        if genre not in genres2:
            genres2 += ", " + genre

    return genres2

def load_api_movies():
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

    stravdf = load_csv("../datasets/strav_dataset.csv")
    stravdf.rename(columns = {'tmdbID':'id'}, inplace = True)
    stravdf.drop(["overview"], axis=1, inplace=True)
    stravdf.drop(["originalLanguage"], axis=1, inplace=True)
    stravdf.drop(["year"], axis=1, inplace=True)

    tmdbdf = load_csv("../datasets/tmdb_dataset.csv")
    tmdbdf.drop(["title"], axis=1, inplace=True)
    tmdbdf.drop(["vote_average"], axis=1, inplace=True)
    tmdbdf.drop(["popularity"], axis=1, inplace=True)

    df = pd.merge(stravdf, tmdbdf, on="id")

    # unnecessary column
    df.drop(["id"], axis=1, inplace=True)

    # compare genres on both datasets
    for i, row in df.iterrows():
        if df.at[i,'genres'] != df.at[i,'genre_ids']:
            df.at[i,'genres'] = equalize_genres(df.at[i,'genres'], df.at[i,'genre_ids'])
    
    df.drop(["genre_ids"], axis=1, inplace=True)

    # now integrate utelly

    utellydf = load_csv("../datasets/utelly_dataset.csv")
    utellydf.drop(["name"], axis=1, inplace=True)

    df.rename(columns = {'imdbID':'id'}, inplace = True)
    df = pd.merge(df, utellydf, on="id")

    # iterate, unify streaming services and rating
    for i, row in df.iterrows():
        if df.at[i,'streamingInfo.disney.us.added'] > 0:
            if "Disney+" not in str(df.at[i,'streaming_services']):
                df.at[i,'streaming_services'] = str(df.at[i,'streaming_services']) + ", Disney+"
        if df.at[i,'streamingInfo.paramount.us.added'] > 0:
            if "Paramount+" not in str(df.at[i,'streaming_services']):
                df.at[i,'streaming_services'] = str(df.at[i,'streaming_services']) + ", Paramount+"
        if df.at[i,'streamingInfo.showtime.us.added'] > 0:
            if "Showtime" not in str(df.at[i,'streaming_services']):
                df.at[i,'streaming_services'] = str(df.at[i,'streaming_services']) + ", Showtime"
        if df.at[i,'streamingInfo.hulu.us.added'] > 0:
            if "Hulu" not in str(df.at[i,'streaming_services']):
                df.at[i,'streaming_services'] = str(df.at[i,'streaming_services']) + ", Hulu"
        if df.at[i,'streamingInfo.hulu.us.added'] > 0:
            if "Netflix" not in str(df.at[i,'streaming_services']):
                df.at[i,'streaming_services'] = str(df.at[i,'streaming_services']) + ", Netflix"
        if df.at[i,'streamingInfo.prime.us.added'] > 0:
            if "Amazon Prime Video" not in str(df.at[i,'streaming_services']):
                df.at[i,'streaming_services'] = str(df.at[i,'streaming_services']) + ", Amazon Prime Video"
        if df.at[i,'streamingInfo.hbo.us.added'] > 0:
            if "HBO Max" not in str(df.at[i,'streaming_services']):
                df.at[i,'streaming_services'] = str(df.at[i,'streaming_services']) + ", HBO Max"
        if df.at[i,'streamingInfo.zee5.us.added'] > 0:
            if "ZEE5" not in str(df.at[i,'streaming_services']):
                df.at[i,'streaming_services'] = str(df.at[i,'streaming_services']) + ", ZEE5"
        if df.at[i,'streamingInfo.peacock.us.added'] > 0:
            if "Peacock" not in str(df.at[i,'streaming_services']):
                df.at[i,'streaming_services'] = str(df.at[i,'streaming_services']) + ", Peacock"
        if df.at[i,'streamingInfo.starz.us.added'] > 0:
            if "Starz" not in str(df.at[i,'streaming_services']):
                df.at[i,'streaming_services'] = str(df.at[i,'streaming_services']) + ", Starz"
        if df.at[i,'streamingInfo.mubi.us.added'] > 0:
            if "Starz" not in str(df.at[i,'streaming_services']):
                df.at[i,'streaming_services'] = str(df.at[i,'streaming_services']) + ", Mubi"
        if df.at[i,'streamingInfo.apple.us.added'] > 0:
            if "AppleTV+" not in str(df.at[i,'streaming_services']):
                df.at[i,'streaming_services'] = str(df.at[i,'streaming_services']) + ", AppleTV+"
        df.at[i,'imdbRating'] = (df.at[i,'imdbRating'] + df.at[i,'tmdbRating'])/2
    
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
    
    df.rename(columns = {'posterURLs.original':'poster'}, inplace = True)
    df.drop(["tmdbRating"], axis=1, inplace=True)
    df.rename(columns = {'imdbRating':'rating'}, inplace = True)

    new_movies = 0
    updated_movies = 0
    for i, row in df.iterrows():
        try:
            genres = []
            if not pd.isna(row["genres"]):
                genres = insert_genres(row["genres"].split(", "))

            movie = Movie.get_by_title(row["title"])

            if movie is None:
                movie = Movie(
                    title=row["title"],
                    country=row["countries"], # es un string de lista? formatear
                    release_year=row["release_date"], # formatear
                    duration=row["runtime"],
                    description=row["overview"],
                    # rating=row["rating"]
                )
                new_movies += 1
                movie.save(row["streaming_services"].split(", "), genres)
            else:
                updated_movies += 1
                movie.update(row["streaming_services"].split(", "), genres)
        except Exception as e:
            print(e)
            print("Error adding movie: " + row["title"])

    print("New movies: " + str(new_movies))
    print("Updated movies: " + str(updated_movies))

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
    time = datetime.now()
    load_api_movies()
    print("APIs: " + str(datetime.now() - time))
