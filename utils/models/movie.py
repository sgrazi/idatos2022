from db import SingletonDatabase
from sqlalchemy.orm import relationship
from datetime import datetime

db = SingletonDatabase.get_instance()


class MovieGenre(db.Base):
    __tablename__ = "movies_genres"
    __table_args__ = {"autoload": True}
    genre = relationship("Genre")


class MoviePlatform(db.Base):
    __tablename__ = "movies_platforms"
    __table_args__ = {"autoload": True}
    platform = relationship("Platform")


class Movie(db.Base):
    __tablename__ = "movies"
    __table_args__ = {"autoload": True}

    genres = relationship("MovieGenre")
    platforms = relationship("MoviePlatform")

    def __repr__(self):
        return f"Movie(id={self.id}, title={self.title}, country={self.country}, release_year={self.release_year}, duration={self.duration}, description={self.description}, image={self.image})"

    @staticmethod
    def get_by_id(id):
        return db.session.query(Movie).filter(Movie.id == id).first()

    @staticmethod
    def get_by_title(title):
        return db.session.query(Movie).filter(Movie.title == title).first()

    @staticmethod
    def get_all():
        return db.session.query(Movie).all()

    def save(self, platforms, genres):
        try:

            db.session.add(self)
            db.session.flush()
            movie_id = self.id
            for platform in platforms:
                movie_platform = MoviePlatform()
                movie_platform.movie_id = movie_id
                movie_platform.platform_id = platform.id
                db.session.add(movie_platform)

            for genre in genres:
                movie_genre = MovieGenre()
                movie_genre.movie_id = movie_id
                movie_genre.genre_id = genre.id
                db.session.add(movie_genre)

            db.session.commit()
        except Exception as e:
            print(e)
            db.session.rollback()
            print(f"Error al crear la película {self.title}")

    def update(self, platforms, genres):
        try:
            for platform in platforms:
                filtered = list(
                    filter(lambda x: x.platform.id == platform.id, self.platforms)
                )
                if len(filtered) == 0:
                    movie_platform = MoviePlatform()
                    movie_platform.movie_id = self.id
                    movie_platform.platform_id = platform.id
                    db.session.add(movie_platform)

            for genre in genres:
                filtered = list(filter(lambda x: x.genre.id == genre.id, self.genres))
                if len(filtered) == 0:
                    movie_genre = MovieGenre()
                    movie_genre.movie_id = self.id
                    movie_genre.genre_id = genre.id
                    db.session.add(movie_genre)

            self.updated_at = datetime.now()
            # db.session.refresh()
            db.session.commit()
        except Exception as e:
            print(e)
            db.session.rollback()
            print(f"Error al actualizar la película {self.title}")
