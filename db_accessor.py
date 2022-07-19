import sqlite3

class DBAccessor:
    def __init__(self, db_name: str, in_memory:bool):
        self.connection = self.create_connection(db_name, in_memory)
        
    def create_connection(self, db_name: str, in_memory: bool):
        connection = None
        try:
            if in_memory:
                connection = sqlite3.connect(':memory:')
            else:
                connection = sqlite3.connect(db_name)
            return connection
        except Exception as e:
            print(e)

        return connection

    def create_table(self, sql):
        try:
            conn = self.connection.cursor()
            conn.execute(sql)
        except Exception as e:
            print(e)
    
    def commit_changes(self):
        try:
            self.connection.commit()
        except Exception as e:
            print(e)
    
    def get_cursor(self):
        try:
            return self.connection.cursor()
        except Exception as e:
            print(e)

