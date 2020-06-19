from flask import request, render_template, Blueprint
from flask_restful import Resource, marshal

from grocery_store.models import Good
from grocery_store.database import db
from grocery_store.routes.marshal_structure import goods_structure

goods_page = Blueprint("goods_page", __name__)


@goods_page.route('/goods_page')
def get_all_goods():
    return render_template('goods-page.html', goods=Good.query.all())


class Goods(Resource):
    def get(self, good_id=None):
        if good_id:
            good = Good.query.get(good_id)
            if good:
                return marshal(good, goods_structure)
            return f"No such good with id: {good_id}"
        return marshal(Good.query.all(), goods_structure)

    def post(self):
        good = Good(**request.json)
        db.session.add(good)
        db.session.commit()
        return f"Successfully added a new good {good}"

    def put(self, good_id):
        good = Good.query.get(good_id)
        good.name = request.json.get("name", good.name)
        good.brand = request.json.get("brand", good.brand)
        good.price = request.json.get("price", good.price)
        db.session.commit()
        return f"Successfully updated Good with id: {good_id}"

    def delete(self, good_id):
        good = Good.query.get(good_id)
        db.session.delete(good)
        db.session.commit()
        return f"Successfully deleted User with id: {good_id}"
