import sqlite3

class ItemModel:
    def __init__(self, name, price):
        self.name = name
        self.price = price

    def json(self):
        return {'name': self.name, 'proce': self.price}

    @classmethod
    def find_by_name(cls, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        result = cursor.execute("SELECT * from items WHERE name = ?", (name,))
        item = result.fetchone()
        connection.close()

        if item:
            return cls(item[0], item[1]) # or cls(*item)

    def create(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        cursor.execute("INSERT INTO items VALUES (?, ?)", (self.name, self.price))
        connection.commit()
        connection.close()

    def update(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        cursor.execute("UPDATE items SET price=? WHERE name=?", (self.price, self.name))
        connection.commit()
        connection.close()
