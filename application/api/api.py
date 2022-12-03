from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from models import load_tables
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import relationship

app = Flask(__name__)
app.config.from_pyfile(filename="config.py")
db = SQLAlchemy(app)
with app.app_context():
    Base = automap_base()

    tables = load_tables(base=Base)
    Base.prepare(db.engine, reflect=True)


@app.route("/movies")
def list_movies():
    args = request.args.to_dict()
    title = args.get("title")
    movieList = []
    Movie = tables["Movies"]
    if title:
        movies = db.session.query(Movie).filter(Movie.title.like(f"%{title}%")).all()
    else:
        movies = db.session.query(Movie).limit(20).all()

    for movie in movies:
        movieList.append(movie.json())

    return {"movies": movieList}


@app.route("/movies/<id>")
def get_movie_by_id(id):
    Movie = tables["Movies"]
    movie = db.session.query(Movie).filter(Movie.id == id).first()


    return {"movie": movie.json()}


if __name__ == "__main__":
    app.run(debug=True, port=5001)
