import json
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

import raw_data

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_AS_ASCII'] = False

db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    age = db.Column(db.Integer)
    email = db.Column(db.String(100))
    role = db.Column(db.String(100))
    phone = db.Column(db.String(20))

    def to_dict(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "age": self.age,
            "email": self.email,
            "role": self.role,
            "phone": self.phone
        }


class Order(db.Model):
    __tablename__ = 'order'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.String)
    start_date = db.Column(db.String)
    end_date = db.Column(db.String)
    address = db.Column(db.String)
    price = db.Column(db.Integer)
    customer_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    executor_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "address": self.address,
            "price": self.price,
            "customer_id": self.customer_id,
            "executor_id": self.executor_id
        }


class Offer(db.Model):
    __tablename__ = "offer"
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey("order.id"))
    executor_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    def to_dict(self):
        return {
            "id": self.id,
            "order_id": self.order_id,
            "executor_id": self.executor_id
        }


# db.drop_all() # uncomment when creating db in a file, not in memory
db.create_all()

for user_data in raw_data.users:
    new_user = User(
        id=user_data["id"],
        first_name=user_data["first_name"],
        last_name=user_data["last_name"],
        age=user_data["age"],
        email=user_data["email"],
        role=user_data["role"],
        phone=user_data["phone"]
    )
    db.session.add(new_user)
    db.session.commit()

for order_data in raw_data.orders:
    new_order = Order(
        id=order_data["id"],
        name=order_data["name"],
        description=order_data["description"],
        start_date=order_data["start_date"],
        end_date=order_data["end_date"],
        address=order_data["address"],
        price=order_data["price"],
        customer_id=order_data["customer_id"],
        executor_id=order_data["executor_id"]
    )
    db.session.add(new_order)
    db.session.commit()

for offer_data in raw_data.offers:
    new_offer = Offer(
        id=offer_data["id"],
        order_id=offer_data["order_id"],
        executor_id=offer_data["executor_id"]
    )
    db.session.add(new_offer)
    db.session.commit()


@app.route("/users", methods=['GET', 'POST'])
def users():
    if request.method == "GET":
        results = []
        for user in User.query.all():
            results.append(user.to_dict())
        return jsonify(results), 200


@app.route("/users/<int:uid>", methods=['GET'])
def get_user(uid):
    user = User.query.get(uid)
    if user:
        return jsonify(user.to_dict()), 200
    else:
        return f"No user found with id: {uid}", 404


@app.route("/orders", methods=['GET', 'POST'])
def orders():
    if request.method == "GET":
        results = []
        for order in Order.query.all():
            results.append(order.to_dict())
        return jsonify(results), 200


@app.route("/orders/<int:oid>", methods=['GET'])
def get_order(oid):
    order = Order.query.get(oid)
    if order:
        return jsonify(order.to_dict()), 200
    else:
        return f"No order found with id: {oid}", 404


@app.route("/offers", methods=['GET', 'POST'])
def offers():
    if request.method == "GET":
        results = []
        for offer in Offer.query.all():
            results.append(offer.to_dict())
        return jsonify(results), 200


@app.route("/offers/<int:ofid>", methods=['GET'])
def get_offer(ofid):
    offer = Offer.query.get(ofid)
    if offer:
        return jsonify(offer.to_dict()), 200
    else:
        return f"No offer found with id: {ofid}", 404


if __name__ == "__main__":
    app.run(debug=True)
