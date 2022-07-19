from db_accessor import DBAccessor

def create_tables(accessor):

    sql_create_artist_table = """ CREATE TABLE IF NOT EXISTS artist (
                                        id integer PRIMARY KEY,
                                        name text NOT NULL
                                    ); """

    sql_create_album_table = """CREATE TABLE IF NOT EXISTS album (
                                    id integer PRIMARY KEY,
                                    name text NOT NULL,
                                    release_date text NOT NULL,
                                    price real NOT NULL,
                                    artist_id integer NOT NULL,
                                    FOREIGN KEY (artist_id) REFERENCES artist (id)
                                );"""

    sql_create_track_table = """CREATE TABLE IF NOT EXISTS track (
                                    id integer PRIMARY KEY,
                                    title text NOT NULL,
                                    duration text NOT NULL,
                                    album_id integer NOT NULL,
                                    FOREIGN KEY (album_id) REFERENCES album (id)
                                );"""


    if accessor.connection is not None:
        accessor.create_table(sql_create_artist_table)
        accessor.create_table(sql_create_album_table)
        accessor.create_table(sql_create_track_table)
    else:
        print("Encoutnered error while trying to create tables.")

def init_db(name: str, in_memory: bool):
    db_accessor = DBAccessor(name, in_memory=in_memory)
    create_tables(db_accessor)
    return db_accessor

if __name__ == '__main__':
    db_accessor = DBAccessor("itunes_db.sql")
    create_tables("itunes_db.sql")