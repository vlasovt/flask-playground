import sqlite3

connection = sqlite3.connect('data.db')
cursor = connection.cursor()

create_table = "CREATE TABLE users(id int, username text, password text)"
cursor.execute(create_table)

user = (1, 'jose', 'asdf')
create_user = "INSERT INTO users VALUES (?, ?, ?)"
cursor.execute(create_user, user)

users = [
    (2, 'john', '1245'),
    (3, 'bob', '53453'),
    (4, 'martha', 'fsfds')
]

cursor.executemany(create_user, users)

select_query = "SELECT * FROM users"
for row in cursor.execute(select_query):
    print(row)

connection.commit()
connection.close()