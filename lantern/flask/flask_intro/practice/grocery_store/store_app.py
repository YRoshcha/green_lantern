import inject
from flask import Flask, jsonify, request


class NoSuchUserError(Exception):
    def __init__(self, user_id):
        self.message = f'No such user_id {user_id}'


class NoSuchStoreError(Exception):
    def __init__(self, store_id):
        self.message = f'No such store_id {store_id}'


app = Flask(__name__)


@app.errorhandler(NoSuchStoreError)
@app.errorhandler(NoSuchUserError)
def my_error_handler(e):
    return jsonify({'error': e.message}), 404


@app.route('/users', methods=['POST'])
def create_user():
    db = inject.instance('DB')
    user_id = db.users.add(request.json)
    return jsonify({'user_id': user_id}), 201


@app.route('/users/<int:user_id>')
def get_user(user_id):
    db = inject.instance('DB')
    user = db.users.get_user_by_id(user_id)
    return jsonify(user)


@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    db = inject.instance('DB')
    db.users.update_user_by_id(user_id, request.json)
    return jsonify({'status': 'success'})


@app.route('/goods', methods=['POST'])
def create_goods():
    db = inject.instance('DB')
    count_of_goods = db.goods.add(request.json)
    return jsonify({'numbers of items created': count_of_goods}), 201


@app.route('/goods')
def get_product():
    db = inject.instance('DB')
    goods = db.goods.get_product()
    return jsonify(goods)


@app.route('/goods', methods=['PUT'])
def update_goods():
    db = inject.instance('DB')
    succesful_update, error_update = db.goods.update_product(request.json)
    return jsonify({'successfully_updated': succesful_update, 'errors': {'no such id in goods': error_update}})


@app.route('/stores', methods=['POST'])
def create_store():
    db = inject.instance('DB')
    db.users.get_user_by_id(request.json["manager_id"])
    store_id = db.stores.add(request.json)
    return jsonify({'store_id': store_id}), 201


@app.route('/stores/<int:store_id>')
def get_store(store_id):
    db = inject.instance('DB')
    store = db.stores.get_store_by_id(store_id)
    return jsonify(store)


@app.route('/stores/<int:store_id>', methods=['PUT'])
def update_store(store_id):
    db = inject.instance('DB')
    db.users.get_user_by_id(request.json["manager_id"])
    db.stores.update_store_by_id(store_id, request.json)
    return jsonify({'status': 'success'})
