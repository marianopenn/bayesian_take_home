
class RequestHandler:
    def __init__(self, connection):
        self.connection = connection

    def create_artist(self, name: str) -> int:
        cursor = self.connection.get_cursor()
        insert_artist = '''INSERT INTO artist (name) VALUES (?)'''
        cursor.execute(insert_artist, (name,))
        self.connection.commit_changes()
        return cursor.lastrowid
    
    def get_artists(self):
        cursor = self.connection.get_cursor()
        list_artists = '''SELECT name from artist'''
        result = cursor.execute(list_artists)
        return result.fetchall()
    
    def get_artist_id(self, name: str):
        cursor = self.connection.get_cursor()
        get_artist_id = '''SELECT id from artist WHERE name=(?)'''
        result = cursor.execute(get_artist_id, (name,))
        try:
            return result.fetchone()[0]
        except KeyError as e:
            return None
        except Exception as e:
            print(f"Unexpected exception while retrieving artist id for {name}.")
            return None

    def create_album(self, title: str, release_date: str, price: float, artist_name: str, tracks=None):
        artist_id = self.get_artist_id(artist_name)
        if not artist_id:
            print(f"Cannot create an album for a non-existent artist={artist_name}")
            return None
        cursor = self.connection.get_cursor()
        insert_album = '''INSERT INTO album (title, release_date, price, artist_id) VALUES (?,?,?,?);'''
        cursor.execute(insert_album, (title, release_date, price, artist_id))
        if tracks:
            self.add_tracks(title, tracks, cursor.lastrowid)
        self.connection.commit_changes()
        return cursor.lastrowid
    
    def get_album_id(self, album_title: str) -> int:
        cursor = self.connection.get_cursor()
        get_album_id = '''SELECT id from album WHERE title=(?);'''
        result = cursor.execute(get_album_id, (album_title,))
        try:
            return result.fetchone()[0]
        except KeyError as e:
            return None
        except Exception as e:
            print(f"Unexpected exception while retrieving album id for {album_title}.")
            return None
    
    def get_albums_for_artist(self, artist_name: str, provide_tracklist=False, filter_price=None, filter_release_date=None):
        artist_id = self.get_artist_id(artist_name)
        if not artist_id:
            print(f"Cannot create an album for a non-existent artist={artist_name}")
            return None
        cursor = self.connection.get_cursor()
        get_albums = '''SELECT title, release_date, price FROM album WHERE artist_id=?'''
        result = cursor.execute(get_albums, (artist_id,))
        albums = result.fetchall()
        if filter_price:
            albums = [(album_name, release_date, price) for album_name, release_date, price in albums if price == filter_price]
        if filter_release_date:
            albums = [(album_name, release_date, price) for album_name, release_date, price in albums if release_date == filter_release_date]
        if provide_tracklist:
            albums_with_tracks = []
            for album_name, release_date, price in albums:
                tracks = self.get_tracks(album_name)
                albums_with_tracks.append((album_name, release_date, price, tracks))
            return albums_with_tracks
        else:
            return albums



    def get_albums_for_artist_by_price(self, artist_name: str, price: float):
        artist_id = self.get_artist_id(artist_name)
        if not artist_id:
            print(f"Cannot create an album for a non-existent artist={artist_name}")
            return None
        cursor = self.connection.get_cursor()
        get_albums = '''SELECT title, release_date, price FROM album WHERE artist_id=? AND price=?;'''
        result = cursor.execute(get_albums, (artist_id,price,))
        return result.fetchall()
    
    def get_albums_for_artist_by_release(self, artist_name: str, release_date):
        artist_id = self.get_artist_id(artist_name)
        if not artist_id:
            print(f"Cannot create an album for a non-existent artist={artist_name}")
            return None
        cursor = self.connection.get_cursor()
        get_albums = '''SELECT title, release_date, price FROM album WHERE artist_id=? AND release_date=?;'''
        result = cursor.execute(get_albums, (artist_id,release_date,))
        return result.fetchall()

    def add_tracks(self, album_title: str, tracks, album_id=None):
        if not album_id:
            album_id = self.get_album_id(album_title)
        if not album_id:
            print(f"Cannot create a track for a non-existent album={album_title}")
            return None
        tracks = [(track[0], track[1], track[2], album_id) for track in tracks]
        add_tracks = '''INSERT INTO track (title, minutes, seconds, album_id) VALUES (?, ?, ?, ?);'''
        cursor = self.connection.get_cursor()
        cursor.executemany(add_tracks, tracks)
        self.connection.commit_changes()
    
    def get_tracks(self, album_title: str):
        album_id = self.get_album_id(album_title)
        if not album_id:
            print(f"No tracks for album={album_title}")
            return []
        get_tracks = '''SELECT title, minutes, seconds FROM track WHERE album_id=(?);'''
        cursor = self.connection.get_cursor()
        result = cursor.execute(get_tracks, (album_id,))
        return result.fetchall()
        
