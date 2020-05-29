import sqlite3

connection = sqlite3.connect('data.db')
cursor = connection.cursor()

create_table = "CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY, username text, password text)"
cursor.execute(create_table)

create_table = "CREATE TABLE IF NOT EXISTS items(name text, price real)"
cursor.execute(create_table)

# items = [
#     ('book', 12.88),
#     ('pencil', 33.22),
#     ('carpet', 100.33)
# ]

# create_item= "INSERT INTO items VALUES (?, ?)"
# cursor.executemany(create_item, items)

# select_query = "SELECT * FROM users"
# for row in cursor.execute(select_query):
#     print(row)

connection.commit()
connection.close()