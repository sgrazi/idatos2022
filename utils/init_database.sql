DROP TABLE IF EXISTS movies;

CREATE TABLE movies(
	id  VARCHAR ( 50 ) PRIMARY KEY,
	title VARCHAR ( 50 ) NOT NULL,
	country VARCHAR ( 50 ),
	release_year VARCHAR ( 50 ),
	duration VARCHAR(20),
	description TEXT
);