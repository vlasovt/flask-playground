import sqlite3
from flask_restful import Resource, reqparse
from models.user import User

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