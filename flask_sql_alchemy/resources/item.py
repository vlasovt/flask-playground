import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel

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
        item = ItemModel.find_by_name(name)
        if item:
            return item.json, 200
        else:
            return {'message': 'Item is not found'}, 404

    def post(self, name):

        if ItemModel.find_by_name(name):
            return {'message': f'the item with name {name} already exists'}, 400

        data = Item.parser.parse_args()

        item = ItemModel(name, data['price'])

        try:
            item.create()
        except:
            return {'message': 'Insert item failed'}, 500

        return item.json, 201

    def delete(self, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        cursor.execute("DELETE FROM items WHERE name = ?", (name,))
        connection.commit()
        connection.close()
        return {'message': f'the item with name {name} has been deleted'}, 204

    def put(self, name):
        data = Item.parser.parse_args()

        item = ItemModel.find_by_name(name)
        updated_item = ItemModel(name, data['price'])

        if item is None:
            try:
                updated_item.create()
            except:
                return {'message': 'Insert item failed'}, 500
        else:
            try:
                updated_item.update()
            except:
                return {'message': 'Update item failed'}, 500
        return updated_item.json, 201


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
