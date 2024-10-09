
DROP TABLE IF EXISTS game_listing, game_os_assignment, game_genre_assignment, game ;
DROP TABLE IF EXISTS operating_system, platform, genre, subscriber ;


CREATE TABLE subscriber (
    sub_id INT GENERATED ALWAYS AS IDENTITY,
    sub_name VARCHAR(40) NOT NULL,
    sub_email VARCHAR(100) NOT NULL UNIQUE,
PRIMARY KEY (sub_id)
);

CREATE TABLE genre (
    genre_id SMALLINT GENERATED ALWAYS AS IDENTITY,
    genre_name VARCHAR(50) NOT NULL UNIQUE,
PRIMARY KEY (genre_id)
);

CREATE TABLE platform (
    platform_id SMALLINT GENERATED ALWAYS AS IDENTITY,
    platform_name VARCHAR(10) NOT NULL UNIQUE,
PRIMARY KEY (platform_id)
);

CREATE TABLE operating_system (
    os_id SMALLINT GENERATED ALWAYS AS IDENTITY,
    os_name VARCHAR(60) NOT NULL UNIQUE,
PRIMARY KEY (os_id)
);

CREATE TABLE game (
    game_id INT GENERATED ALWAYS AS IDENTITY,
    game_title TEXT NOT NULL ,
    game_description TEXT ,
    release_date TIMESTAMPTZ NOT NULL, 
    is_NSFW BOOLEAN ,
    image_URL TEXT , 
PRIMARY KEY (game_id)
);

CREATE TABLE game_genre_assignment (
    assignment_id INT GENERATED ALWAYS AS IDENTITY,
    game_id INT NOT NULL UNIQUE ,
    genre_id SMALLINT NOT NULL UNIQUE,
PRIMARY KEY (assignment_id),
FOREIGN KEY (game_id) REFERENCES game(game_id),
FOREIGN KEY (genre_id) REFERENCES genre(genre_id)
);

CREATE TABLE game_os_assignment (
    assignment_id INT GENERATED ALWAYS AS IDENTITY,
    game_id INT NOT NULL UNIQUE ,
    os_id SMALLINT NOT NULL UNIQUE,
PRIMARY KEY (assignment_id),
FOREIGN KEY (game_id) REFERENCES game(game_id),
FOREIGN KEY (os_id) REFERENCES operating_system(os_id)
);

CREATE TABLE game_listing (
    listing_id INT GENERATED ALWAYS AS IDENTITY,
    game_id INT NOT NULL UNIQUE ,
    platform_id SMALLINT NOT NULL UNIQUE,
    release_price INT NOT NULL , 
    listing_date TIMESTAMPTZ NOT NULL, 
    listing_url TEXT NOT NULL UNIQUE , 
PRIMARY KEY (listing_id),
FOREIGN KEY (game_id) REFERENCES game(game_id),
FOREIGN KEY (platform_id) REFERENCES platform(platform_id)
);



