import sqlite3
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required

items = []

class Item(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type=float,
        required=True,
        help='This field cannot be blank!'
    )

    @jwt_required()
    def get(self, name):
         #item = next(filter(lambda x: x['name'] == name, items), None)
        item = Item.find_by_name(name)
        if item:
            return item, 200
        else:
            return {'message': 'Item is not found'}, 404

    @classmethod
    def find_by_name(cls, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        result = cursor.execute("SELECT * from items WHERE name = ?", (name,))
        item = result.fetchone()
        connection.close()

        if item:
            return {"item": {'name': item[0], 'price': item[1]}}

    @classmethod
    def create(cls, item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        cursor.execute("INSERT INTO items VALUES (?, ?)", (item['name'], item['price']))
        connection.commit()
        connection.close() 
    
    @classmethod
    def update(cls, item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        cursor.execute("UPDATE items SET price=? WHERE name=?", (item['price'], item['name']))
        connection.commit()
        connection.close()

    def post(self, name):

        if Item.find_by_name(name):
            return {'message': f'the item with name {name} already exists'}, 400
             
        data = Item.parser.parse_args()
             
        item =  {
            'name': name,
            'price': data['price']
        }
        try:
            Item.create(item)
        except:
            return {'message': 'Insert item failed'}, 500

        return item, 201 
    
    def delete(self, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        cursor.execute("DELETE FROM items WHERE name = ?", (name,))
        connection.commit()
        connection.close()
        return {'message': f'the item with name {name} has been deleted'}, 204

    def put(self, name):
        data = Item.parser.parse_args()

        item = Item.find_by_name(name)
        updated_item =  {'name': name,'price': data['price']}
        
        if item is None:
            try:
                Item.create(updated_item)
            except:
                return {'message': 'Insert item failed'}, 500
        else:
            try:
                Item.update(updated_item)
            except:
                return {'message': 'Update item failed'}, 500
        return updated_item, 201 


class ItemList(Resource):

    def get(self):
        items = []
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        result = cursor.execute("SELECT * FROM items")
        for row in result:
            items.append({'name': row[0], 'price': row[1]})

        connection.close()
        return {'items': items}