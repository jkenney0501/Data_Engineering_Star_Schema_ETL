# DROP TABLES as needed
songplay_table_drop = "DROP TABLE IF EXISTS songplays"
user_table_drop = "DROP TABLE IF EXISTS users"
song_table_drop = "DROP TABLE IF EXISTS songs"
artist_table_drop = "DROP TABLE IF EXISTS artists"
time_table_drop = "DROP TABLE IF EXISTS time"


# CREATE TABLES - Foreign Keys aadded later with ALTER statment below.

songplay_table_create = ("""CREATE TABLE IF NOT EXISTS songplays
                        (songplay_id SERIAL PRIMARY KEY, 
                        start_time timestamp NOT NULL, 
                        user_id INT NOT NULL, 
                        level varchar(50), 
                        song_id varchar(255), 
                        artist_id varchar(255), 
                        session_id INT NOT NULL, 
                        location varchar(255), 
                        user_agent varchar(255))
                        """)


user_table_create = ("""CREATE TABLE IF NOT EXISTS users
                    (user_id INT PRIMARY KEY, 
                    first_name varchar(255), 
                    last_name varchar(255), 
                    gender varchar(10), 
                    level varchar(50))
                    """)


song_table_create = ("""CREATE TABLE IF NOT EXISTS songs
                    (song_id varchar(255) NOT NULL PRIMARY KEY, 
                    title varchar(255) NOT NULL, 
                    artist_id varchar(255) NOT NULL, 
                    year INT NOT NULL, 
                    duration FLOAT8 NOT NULL)
                    """)

artist_table_create = ("""CREATE TABLE IF NOT EXISTS artists
                    (artist_id varchar(200) NOT NULL PRIMARY KEY, 
                    name varchar(255) NOT NULL, 
                    location varchar(255), 
                    latitude FLOAT8, 
                    longitude FLOAT8)
                    """)

time_table_create = ("""CREATE TABLE IF NOT EXISTS time
                    (start_time timestamp PRIMARY KEY NOT NULL, 
                    hour INT, day INT, 
                    week INT, 
                    month INT, 
                    year INT, 
                    weekday INT)
                    """)





# INSERT RECORDS
songplay_table_insert = ("""INSERT INTO songplays (start_time, user_id, level, song_id, artist_id, session_id, location, user_agent) \
                         VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                         ON CONFLICT (songplay_id) DO NOTHING;
                        """)

# Requires a DO UPDATE because the user level can chnage from free to paid which can cause a PK conflict.
user_table_insert = ("""INSERT INTO users (user_id, first_name, last_name, gender, level) \
                     VALUES (%s, %s, %s, %s, %s)
                     ON CONFLICT (user_id) DO UPDATE SET level=EXCLUDED.level
                    """)

song_table_insert = ("""INSERT INTO songs (song_id, title, artist_id, year, duration) \
                     VALUES (%s, %s, %s, %s, %s)
                     ON CONFLICT (song_id) DO NOTHING;
                    """)

artist_table_insert = ("""INSERT INTO artists (artist_id, name, location, latitude, longitude) \
                     VALUES (%s, %s, %s, %s, %s)
                     ON CONFLICT (artist_id) DO NOTHING;
                    """)


time_table_insert = ("""INSERT INTO time (start_time, hour, day, week, month, year, weekday)
                     VALUES (%s, %s, %s, %s, %s, %s, %s)
                     ON CONFLICT (start_time) DO NOTHING;
                    """) 



# Add FORIEGN KEYS to the fact table for and make sure all rows get deleted if one does(within the relationship) by using CASCADE.
add_songplays_fk_user = ("""ALTER TABLE songplays
                         ADD CONSTRAINT fk_user 
                         FOREIGN KEY(user_id) 
                         REFERENCES users(user_id) ON DELETE CASCADE;
                         """)

add_song_fk_song_id = ("""ALTER TABLE songplays
                         ADD CONSTRAINT fk_song 
                         FOREIGN KEY(song_id) 
                         REFERENCES songs(song_id) ON DELETE CASCADE;
                         """)

add_artists_fk_artist_id = ("""ALTER TABLE songplays
                           ADD CONSTRAINT fk_artist 
                           FOREIGN KEY(artist_id) 
                           REFERENCES artists(artist_id) ON DELETE CASCADE;
                           """)
    
add_songplays_fk_start = ("""ALTER TABLE songplays
                         ADD CONSTRAINT fk_time 
                         FOREIGN KEY(start_time) 
                         REFERENCES time(start_time) ON DELETE CASCADE;
                         """)
    
    
# FIND SONGS
song_select = ("""
SELECT s.song_id, a.artist_id
FROM songs as s
JOIN artists as a ON (a.artist_id = s.artist_id)
WHERE s.title = %s AND a.name = %s AND s.duration = %s;
""")


# QUERY LISTS
create_table_queries = [songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create, add_songplays_fk_user, add_song_fk_song_id,add_artists_fk_artist_id, add_songplays_fk_start]
drop_table_queries = [songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]