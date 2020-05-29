import sqlite3

class User:
    def __init__(self, _id, username, password):
        self.id = _id
        self.username = username
        self.password = password

    @classmethod
    def find_by_username(cls, username):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        result = cursor.execute("SELECT * from users WHERE username = ?", (username,))
        user_data = result.fetchone()
        if user_data:
            user = cls(*user_data)
        else:
            user = None
        connection.close()
        return user

    @classmethod
    def find_by_id(cls, _id):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        result = cursor.execute("SELECT * from users WHERE id = ?", (_id,))
        user_data = result.fetchone()
        if user_data:
            user = cls(*user_data)
        else:
            user = None
        connection.close()
        return user