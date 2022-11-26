DROP TABLE IF EXISTS movies CASCADE; 

CREATE TABLE movies(
	id  INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
	title VARCHAR ( 50 ) NOT NULL,
	country VARCHAR ( 50 ),
	release_year VARCHAR ( 50 ),
	duration VARCHAR(20),
	description TEXT
);

DROP TABLE IF EXISTS genres CASCADE;

CREATE TABLE genres(
	id  INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
	name VARCHAR ( 50 ) NOT NULL
);

DROP TABLE IF EXISTS platforms CASCADE;

CREATE TABLE platforms(
	id  INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
	name VARCHAR ( 50 ) NOT NULL
);


DROP TABLE IF EXISTS movies_genres CASCADE;

CREATE TABLE movies_genres(
	movie_id INT REFERENCES movies(id),
	genre_id INT REFERENCES genres(id),
	PRIMARY KEY (movie_id, genre_id)
);

DROP TABLE IF EXISTS movies_platforms CASCADE;

CREATE TABLE movies_platforms(
	movie_id INT REFERENCES movies(id),
	platform_id INT REFERENCES platforms(id),
	PRIMARY KEY (movie_id, platform_id)
);