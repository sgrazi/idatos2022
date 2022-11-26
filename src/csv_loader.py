import pandas as pd

from db import SingletonDatabase
from models import Movie


def load_csv(path):
    return pd.read_csv(path)

def load_movies(df):
    db = SingletonDatabase.get_instance()
    for index, row in df.iterrows():
        movie = Movie()
        movie.id = row['show_id']
        movie.title = row['title']
        movie.director = row['director']
        movie.country = row['country']
        movie.release_year = row['release_year']
        movie.rating = row['rating']
        movie.duration = row['duration']
        movie.description = row['description']

        try:
            db.session.add(movie)
            db.session.commit()
        except Exception as e:
            print(e)
            db.session.rollback()
            print(f"Error al crear el usuario {row['show_id']}")
        
        if index == 5:
            break



if __name__ == '__main__':
    df = load_csv('../datasets/amazon_prime_titles.csv')
    df = df.query('type == "Movie"')
    print(df)
    load_movies(df)

    print(df.describe())
