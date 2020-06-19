import inject
from fake_storage import FakeStorage
from store_app import app


def configure_test(binder):
    db = FakeStorage()
    binder.bind('DB', db)


class Initializer:
    def setup(self):
        inject.clear_and_configure(configure_test)

        app.config['TESTING'] = True
        with app.test_client() as client:
            self.client = client


class TestUsers(Initializer):
    def test_create_new(self):
        resp = self.client.post(
            '/users',
            json={'name': 'John Doe'}
        )
        assert resp.status_code == 201
        assert resp.json == {'user_id': 1}

        resp = self.client.post(
            '/users',
            json={'name': 'Andrew Derkach'}
        )
        assert resp.json == {'user_id': 2}

    def test_successful_get_user(self):
        resp = self.client.post(
            '/users',
            json={'name': 'John Doe'}
        )
        user_id = resp.json['user_id']
        resp = self.client.get(f'/users/{user_id}')
        assert resp.status_code == 200
        assert resp.json == {'name': 'John Doe'}

    def test_get_unexistent_user(self):
        resp = self.client.get(f'/users/1')
        assert resp.status_code == 404
        assert resp.json == {'error': 'No such user_id 1'}

    def test_succesful_update_user(self):
        resp = self.client.post(
            '/users',
            json={'name': 'John Doe'}
        )
        user_id = resp.json['user_id']
        resp = self.client.put(
            f'/users/{user_id}',
            json={'name': 'Johanna Doe'}
        )
        assert resp.status_code == 200
        assert resp.json == {'status': 'success'}

    def test_unexistent_update_user(self):
        resp = self.client.put(
            f'/users/1',
            json={'name': 'Johanna Doe'}
        )
        assert resp.status_code == 404
        assert resp.json == {'error': 'No such user_id 1'}


class TestGoods(Initializer):
    def test_create_new(self):
        resp = self.client.post(
            '/goods',
            json=(
                {'name': 'Chocolate_bar', 'price': 10},
                {'name': 'Cheese', 'price': 109},
                {'name': 'Banana', 'price': 32},
                {'name': 'Milk', 'price': 25},
                {'name': 'Tea', 'price': 42},
                {'name': 'Coffee', 'price': 85},
                {'name': 'Sugar', 'price': 12},
                {'name': 'Salt', 'price': 8},
                {'name': 'Bread', 'price': 17},
                {'name': 'Carrots', 'price': 4}
            )
        )
        assert resp.status_code == 201
        assert resp.json == {'numbers of items created': 10}

    def test_get_product(self):
        resp = self.client.post(
            '/goods',
            json=(
                {'name': 'Chocolate_bar', 'price': 10},
                {'name': 'Cheese', 'price': 109},
                {'name': 'Banana', 'price': 32},
                {'name': 'Milk', 'price': 25},
                {'name': 'Tea', 'price': 42},
                {'name': 'Coffee', 'price': 85},
                {'name': 'Sugar', 'price': 12},
                {'name': 'Salt', 'price': 8},
                {'name': 'Bread', 'price': 17},
                {'name': 'Carrots', 'price': 4}
            )
        )
        resp = self.client.get(f'/goods')
        assert resp.status_code == 200
        assert resp.json == [
            {'name': 'Chocolate_bar', 'price': 10, "id": 1},
            {'name': 'Cheese', 'price': 109, "id": 2},
            {'name': 'Banana', 'price': 32, "id": 3},
            {'name': 'Milk', 'price': 25, "id": 4},
            {'name': 'Tea', 'price': 42, "id": 5},
            {'name': 'Coffee', 'price': 85, "id": 6},
            {'name': 'Sugar', 'price': 12, "id": 7},
            {'name': 'Salt', 'price': 8, "id": 8},
            {'name': 'Bread', 'price': 17, "id": 9},
            {'name': 'Carrots', 'price': 4, "id": 10}
        ]

    def test_succesful_update_product(self):
        resp = self.client.post(
            '/goods',
            json=(
                {'name': 'Chocolate_bar', 'price': 10, "id": 1},
                {'name': 'Cheese', 'price': 109, "id": 2},
                {'name': 'Banana', 'price': 32, "id": 3},
                {'name': 'Milk', 'price': 25, "id": 4},
                {'name': 'Tea', 'price': 42, "id": 5},
                {'name': 'Coffee', 'price': 85, "id": 6},
                {'name': 'Sugar', 'price': 12, "id": 7},
                {'name': 'Salt', 'price': 8, "id": 8},
                {'name': 'Bread', 'price': 17, "id": 9},
                {'name': 'Carrots', 'price': 4, "id": 10}
            )
        )
        resp = self.client.put(
            f'/goods',
            json=(
                {'name': 'Chocolate_bar', 'price': 11, "id": 1},
                {'name': 'Cheese', 'price': 86, "id": 2},
                {'name': 'Banana', 'price': 35, "id": 3},
                {'name': 'Potatoes', 'price': 15, "id": 11},
                {'name': 'Cookies', 'price': 86, "id": 14},
                {'name': 'Coconut', 'price': 35, "id": 16},

            )
        )
        assert resp.status_code == 200
        assert resp.json == {'successfully_updated': 3, 'errors': {'no such id in goods': [11, 14, 16]}}


class TestStores(Initializer):
    def test_create_store(self):
        resp = self.client.post(
            '/users',
            json={'name': 'John Doe'}
        )
        resp = self.client.post(
            '/users',
            json={'name': 'Bill Gates'}
        )
        resp = self.client.post(
            '/stores',
            json={'name': 'Mad Cow', 'location': 'Lviv', 'manager_id': 2}
        )
        assert resp.status_code == 201
        assert resp.json == {'store_id': 1}

        resp = self.client.post(
            '/stores',
            json={'name': 'Local Taste', 'location': 'Lviv', 'manager_id': 2}
        )
        assert resp.json == {'store_id': 2}

    def test_successful_get_store(self):
        resp = self.client.post(
            '/users',
            json={'name': 'John Doe'}
        )
        resp = self.client.post(
            '/users',
            json={'name': 'Bill Gates'}
        )
        resp = self.client.post(
            '/stores',
            json={'name': 'Mad Cow', 'location': 'Lviv', 'manager_id': 2}
        )
        store_id = resp.json['store_id']
        resp = self.client.get(f'/stores/{store_id}')
        assert resp.status_code == 200
        assert resp.json == {'name': 'Mad Cow', 'location': 'Lviv', 'manager_id': 2}

    def test_get_unexistent_sore(self):
        resp = self.client.get(f'/stores/1')
        assert resp.status_code == 404
        assert resp.json == {'error': 'No such store_id 1'}

    def test_succesful_update_store(self):
        resp = self.client.post(
            '/users',
            json={'name': 'John Doe'}
        )
        resp = self.client.post(
            '/users',
            json={'name': 'Bill Gates'}
        )
        resp = self.client.post(
            '/stores',
            json={'name': 'Mad Cow', 'location': 'Lviv', 'manager_id': 2}
        )
        store_id = resp.json['store_id']
        resp = self.client.put(
            f'/stores/{store_id}',
            json={'name': 'Local Taste', 'location': 'Lviv', 'manager_id': 2}
        )
        assert resp.status_code == 200
        assert resp.json == {'status': 'success'}

    def test_unexistent_update_store(self):
        resp = self.client.post(
            '/users',
            json={'name': 'John Doe'}
        )
        resp = self.client.put(
            f'/stores/1',
            json={'name': 'Local Taste', 'location': 'Lviv', 'manager_id': 1}
        )
        assert resp.status_code == 404
        assert resp.json == {'error': 'No such store_id 1'}
