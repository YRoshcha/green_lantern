from itertools import count

from store_app import NoSuchUserError, NoSuchStoreError


class FakeStorage:
    def __init__(self):
        self._users = FakeUsers()
        self._goods = FakeGoods()
        self._stores = FakeStores()

    @property
    def users(self):
        return self._users

    @property
    def goods(self):
        return self._goods

    @property
    def stores(self):
        return self._stores


class FakeUsers:
    def __init__(self):
        self._users = {}
        self._id_counter = count(1)

    def add(self, user):
        user_id = next(self._id_counter)
        self._users[user_id] = user
        return user_id

    def get_user_by_id(self, user_id):
        try:
            return self._users[user_id]
        except KeyError:
            raise NoSuchUserError(user_id)

    def update_user_by_id(self, user_id, user):
        if user_id in self._users:
            self._users[user_id] = user
        else:
            raise NoSuchUserError(user_id)


class FakeGoods:
    def __init__(self):
        self._goods = {}
        self._id_counter = count(1)

    def add(self, goods):
        count_add_goods = 0
        for product_id, product in enumerate(goods, start=1):
            product["id"] = product_id
            self._goods[product_id] = product
            count_add_goods += 1
        return count_add_goods

    def get_product(self):
        return [self._goods[i] for i in range(1, len(self._goods) + 1)]

    def update_product(self, goods):
        count_success = 0
        list_error = []
        for i in goods:
            product_id = i['id']
            if product_id in self._goods:
                self._goods[product_id] = i
                count_success += 1
            else:
                list_error.append(product_id)
        return count_success, list_error


class FakeStores:
    def __init__(self):
        self._stores = {}
        self._id_counter = count(1)

    def add(self, store):
        store_id = next(self._id_counter)
        self._stores[store_id] = store
        return store_id

    def get_store_by_id(self, store_id):
        try:
            return self._stores[store_id]
        except KeyError:
            raise NoSuchStoreError(store_id)

    def update_store_by_id(self, store_id, store):
        if store_id in self._stores:
            self._stores[store_id] = store
        else:
            raise NoSuchStoreError(store_id)
