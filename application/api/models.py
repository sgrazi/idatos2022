from sqlalchemy.orm import relationship


def load_tables(base):
    class Genre(base):
        __tablename__ = "genres"

    class Platform(base):
        __tablename__ = "platforms"

    class MovieGenre(base):
        __tablename__ = "movies_genres"
        genre = relationship("Genre")

    class MoviePlatform(base):
        __tablename__ = "movies_platforms"

    class Movie(base):
        __tablename__ = "movies"

        genres = relationship("MovieGenre")
        platforms = relationship("MoviePlatform")

        def json(self):
            genres = []
            pltaforms = []
            for genre in self.genres:
                genres.append(genre.genre.name)

            for platform in self.platforms:
                pltaforms.append(platform.platform.name)

            return {
                "id": self.id,
                "title": self.title,
                "country": self.country,
                "release_year": self.release_year,
                "duration": self.duration,
                "description": self.description,
                "genres": genres,
                "platforms": pltaforms,
            }

    tables = {
        "Genres": Genre,
        "Platforms": Platform,
        "Movies": Movie,
        "MoviesGenres": MovieGenre,
        "MoviesPlatforms": MoviePlatform,
    }

    return tables
