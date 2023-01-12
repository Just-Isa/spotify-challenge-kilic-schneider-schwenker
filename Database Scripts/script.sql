alter table playlist drop constraint IF EXISTS playlist_id;
alter table artist drop constraint IF EXISTS artist_uri;
alter table track drop constraint IF EXISTS track_uri;
alter table album drop constraint IF EXISTS album_uri;
alter table artist drop constraint IF EXISTS artist_uri;
DROP TABLE IF EXISTS playlist CASCADE;
DROP TABLE IF EXISTS track CASCADE;
DROP TABLE IF EXISTS album CASCADE;
DROP TABLE IF EXISTS artist CASCADE;
DROP TABLE IF EXISTS track_pos_playlist CASCADE;

CREATE TABLE playlist (
    playlist_name VARCHAR(255),
    playlist_id INT,
    modified_at INT,
    num_tracks INT,
    num_albums INT,
    num_followers INT,
    collaborative BOOLEAN
);

CREATE TABLE track (
    track_uri VARCHAR(255),
    track_name VARCHAR(255),
    duration_ms INT,
    album_uri VARCHAR(255),
    artist_uri VARCHAR(255)
);

CREATE TABLE album (
    album_uri VARCHAR(255),
    album_name VARCHAR(255)
);

CREATE TABLE artist (
    artist_uri VARCHAR(255),
    artist_name VARCHAR(500)
);

CREATE TABLE track_pos_playlist (
    playlist_id INT,
    track_uri VARCHAR(255),
    track_pos INT
);

ALTER TABLE playlist ADD PRIMARY KEY (playlist_id);
ALTER TABLE track ADD PRIMARY KEY (track_uri);
ALTER TABLE artist ADD PRIMARY KEY (artist_uri);
ALTER TABLE album ADD PRIMARY KEY (album_uri);
ALTER TABLE track_pos_playlist ADD FOREIGN KEY (playlist_id) REFERENCES playlist(playlist_id);
ALTER TABLE track_pos_playlist ADD FOREIGN KEY (track_uri) REFERENCES track(track_uri);
ALTER TABLE track ADD FOREIGN KEY (album_uri) REFERENCES album(album_uri);
ALTER TABLE track ADD FOREIGN KEY (artist_uri) REFERENCES artist(artist_uri);
