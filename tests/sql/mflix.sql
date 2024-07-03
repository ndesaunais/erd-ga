CREATE TABLE IF NOT EXISTS users (
  id VARCHAR PRIMARY KEY,
  name TEXT,
  email TEXT,
  password TEXT,
  preferences JSON NULL
);


CREATE TABLE IF NOT EXISTS theaters (
  id VARCHAR PRIMARY KEY,
  theaterId INT,
  location JSON
);


CREATE TABLE IF NOT EXISTS sessions (
  id VARCHAR PRIMARY KEY,
  user_id VARCHAR,
  jwt TEXT,
  FOREIGN KEY (user_id) REFERENCES users(id)
);


CREATE TABLE IF NOT EXISTS movies (
  id VARCHAR PRIMARY KEY,
  title TEXT NULL,
  year INT NULL,
  runtime INT NULL,
  released TIMESTAMP NULL,
  poster TEXT NULL,
  plot TEXT NULL,
  fullplot TEXT NULL,
  lastupdated TIMESTAMP NULL,
  type TEXT NULL,
  directors JSON NULL,
  imdb JSON NULL,
  casting JSON NULL,
  countries JSON NULL,
  genres JSON NULL,
  tomatoes JSON NULL,
  num_mflix_comments INT NULL,
  rated TEXT NULL,
  awards JSON NULL,
  languages JSON NULL,
  writers JSON NULL,
  metacritic INT NULL
);

CREATE TABLE IF NOT EXISTS comments (
  id VARCHAR PRIMARY KEY,
  movie_id VARCHAR NULL,
  name TEXT NULL,
  email TEXT NULL,
  text TEXT NULL,
  date TIMESTAMP NULL,
  FOREIGN KEY (movie_id) REFERENCES movies(id)
);
