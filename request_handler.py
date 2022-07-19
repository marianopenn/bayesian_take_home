
class RequestHandler:
    def __init__(self, connection):
        self.connection = connection

    def create_artist(self, name: str):
        cursor = self.connection.get_cursor()
        insert_artist = '''INSERT INTO artist (name) VALUES (?)'''
        cursor.execute(insert_artist, (name,))
        self.connection.commit_changes()
    
    def get_artists(self):
        cursor = self.connection.get_cursor()
        list_artists = '''SELECT name from artist'''
        result = cursor.execute(list_artists)
        return result.fetchall()