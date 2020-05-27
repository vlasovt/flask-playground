import sqlite3
from flask_restful import Resource, reqparse

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

class UserRegister(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('username',
        type=str,
        required=True,
        help='This field cannot be blank!'
    )
    parser.add_argument('password',
        type=str,
        required=True,
        help='This field cannot be blank!'
    )

    def post(self):
        data = UserRegister.parser.parse_args()

        if User.find_by_username(data['username']):
            return {'message': 'This user already exists'}, 400

        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        create_user = "INSERT INTO users VALUES (NULL, ?, ?)"
        cursor.execute(create_user, (data['username'], data['password']))

        connection.commit()
        connection.close()

        return {'Message': 'User created successfully'}