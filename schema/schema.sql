
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
    game_id INT NOT NULL  ,
    genre_id SMALLINT NOT NULL ,
PRIMARY KEY (assignment_id),
FOREIGN KEY (game_id) REFERENCES game(game_id),
FOREIGN KEY (genre_id) REFERENCES genre(genre_id)
);

CREATE TABLE game_os_assignment (
    assignment_id INT GENERATED ALWAYS AS IDENTITY,
    game_id INT NOT NULL  ,
    os_id SMALLINT NOT NULL ,
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


INSERT INTO subscriber 
    (sub_name , sub_email )
VALUES
    ( 'Michael Hassan' , 'trainee.michael.hassan@sigmalabs.co.uk' ),
    ( 'Mehrdad Halali' , 'trainee.mehrdad.halali@sigmalabs.co.uk' ),
    ( 'Leon Simpson' , 'trainee.leon.simpson@sigmalabs.co.uk' ),
    ( 'Paula Uusnakki' , 'trainee.paula.uusnakki@sigmalabs.co.uk' )
    ;


INSERT INTO genre 
    (genre_name)
VALUES
    ( 'Indie'),
    ( 'Action'),
    ( 'Casual' ),
    ( 'Adventure'),
    ( 'Simulation'),
    ( 'RPG'),
    ( 'Strategy' ),
    ( 'Action-Adventure'),
    ( 'Sports'),
    ( 'Racing'),
    ( 'Software' ),
    ( 'Early Access'),
    ( 'Free To Play'),
    ( 'Massively Multiplayer')
    ;

INSERT INTO platform 
    (platform_name)
VALUES
    ( 'Steam'),
    ( 'GOG'),
    ( 'Epic')
    ;

INSERT INTO operating_system 
    (os_name)
VALUES
    ( 'Windows'),
    ( 'Mac'),
    ( 'Linux')
    ;



