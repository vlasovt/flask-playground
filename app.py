from flask import Flask, jsonify, request

app = Flask(__name__)

stores = [
    {
        'name': 'First Store',
        'items': [
            {
                'name': 'first item',
                'price': 15.99
            }
        ]
    }
]

@app.route('/store', methods=['POST'])
def create_store():
    request_data = request.get_json()
    new_store =  {
        'name': request_data['name'],
        'items': request_data['items'] or []
    }
    stores.append(new_store)
    return jsonify(new_store)


@app.route('/store')
def get_stores():
    return jsonify({'stores': stores})


@app.route('/store/<string:name>')
def get_store(name):
    store = next((item for item in stores if item['name'] == name), None)
    if store != None:
        return jsonify(store)
    return jsonify({"message": "Store not found"})

@app.route('/store/<string:name>/item', methods=['POST'])
def create_item_in_store(name):
    request_data = request.get_json()
    store = next((item for item in stores if item['name'] == name), None)
    if store != None:
        new_item = {
            'name': request_data['name'],
            'proce': request_data['price']
        }
        store['items'].append(new_item)
        return jsonify(store)
    return jsonify({"message": "Store not found"})

@app.route('/store/<string:name>/item')
def get_items_in_store(name):
    store = next((item for item in stores if item['name'] == name), None)
    if store != None:
        return jsonify({"items": store['items']})
    return jsonify({"message": "Store not found"})

app.run()