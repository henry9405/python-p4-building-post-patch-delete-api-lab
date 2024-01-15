from flask import Flask, request, make_response, jsonify
from flask_migrate import Migrate

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def home():
    return '<h1>Bakery GET-POST-PATCH-DELETE API</h1>'

@app.route('/bakeries')
def bakeries():
    bakeries = [bakery.to_dict() for bakery in Bakery.query.all()]
    return make_response(jsonify(bakeries), 200)

@app.route('/bakeries/<int:id>', methods=['GET', 'PATCH'])
def bakery_by_id(id):
    bakery = Bakery.query.filter_by(id=id).first()

    if bakery is None:
        return make_response(jsonify({'error': 'Bakery not found'}), 404)

    if request.method == 'GET':
        bakery_serialized = bakery.to_dict()
        return make_response(jsonify(bakery_serialized), 200)

    if request.method == 'PATCH':
        data = request.form
        bakery.name = data.get('name', bakery.name)
        db.session.commit()
        bakery_serialized = bakery.to_dict()
        return make_response(jsonify(bakery_serialized), 200)

@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    baked_goods_by_price = BakedGood.query.order_by(BakedGood.price.desc()).all()
    baked_goods_by_price_serialized = [bg.to_dict() for bg in baked_goods_by_price]
    return make_response(jsonify(baked_goods_by_price_serialized), 200)

@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    most_expensive = BakedGood.query.order_by(BakedGood.price.desc()).limit(1).first()
    most_expensive_serialized = most_expensive.to_dict()
    return make_response(jsonify(most_expensive_serialized), 200)

@app.route('/baked_goods', methods=['POST'])
def create_baked_good():
    data = request.form.to_dict()
    new_baked_good = BakedGood(
        name=data['name'],
        description=data['description'],
        price=float(data['price'])
    )
    db.session.add(new_baked_good)
    db.session.commit()
    baked_good_serialized = new_baked_good.to_dict()
    return make_response(jsonify(baked_good_serialized), 201)

@app.route('/baked_goods/<int:id>', methods=['DELETE'])
def delete_baked_good(id):
    baked_good = BakedGood.query.get(id)

    if baked_good is None:
        return make_response(jsonify({'error': 'Baked Good not found'}), 404)

    db.session.delete(baked_good)
    db.session.commit()
    return make_response(jsonify({'message': 'Baked Good deleted successfully'}), 200)

if __name__ == '__main__':
    app.run(port=5555, debug=True)
