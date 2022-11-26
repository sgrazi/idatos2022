import pandas as pd
from models.genre import Genre
from models.movie import Movie
from models.platform import Platform


def load_csv(path):
    return pd.read_csv(path)


def load_movies(df, platform):
    for index, row in df.iterrows():
        genres = []
        for genre_name in row["listed_in"].split(", "):
            genre = Genre.get_by_name(genre_name)
            if genre is None:
                genre = Genre()
                genre.name = genre_name
                genre.save()
            genres.append(genre)
        
        movie = Movie.get_by_title(row['title'])
        if movie is None:
            print("Adding movie: " + row['title'])
            movie = Movie(
                title=row["title"],
                country=row["country"],
                release_year=row["release_year"],
                duration=row["duration"],
                description=row["description"],
            )
            print(row["listed_in"])

            movie.save([platform], genres)
        else:
            print("_________________ ACA __________________")
            print("Movie already exists: " + row['title'])
            movie.update([platform], genres)
        # if index >= 100:
        #     break


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

if __name__ == "__main__":
    # load_amazon_csv("../datasets/amazon_prime_titles.csv")
    # load_netflix_csv("../datasets/netflix_titles.csv")
    # load_hulu_csv("../datasets/hulu_titles.csv")
    # print(df.describe())
    movie = Movie.get_by_title("The Resident")
    print(movie)
    print(movie.platforms)
    for platform in movie.platforms:
        print(platform.platform.name)
    
    print(movie.genres)
    for genre in movie.genres:
        print(genre.genre.name)
    # movie = Movie.get_by_id(7598)
    # # print(Movie.get_by_id(7598))
    # print(movie.genres[0].genre.id)
    # filtered = list(filter(lambda x: x.genre.id == 1, movie.genres))
    # for genres in movie.genres:
    #     print(genres.genre)
    # print(filtered)