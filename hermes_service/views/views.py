from flask_restful import Resource, reqparse
from hermes_service.models.models import OrderModel, UserLoginServices


class Orders(Resource):
    def get(self):
        return {"Orders": [orders.json() for orders in OrderModel.query.all()]}


class Order(Resource):
    fields = reqparse.RequestParser()
    fields.add_argument("id", type=str, required=True, help="id is required!")
    fields.add_argument("username", type=str, required=True, help="username_id is required!")
    fields.add_argument("item_id", type=str, required=True, help="item_id is required!")
    fields.add_argument("item_quantity", type=int, required=True, help="item_quantity is required!")

    def get(self):
        data = Order.fields.parse_args()
        order = OrderModel.find_order(data["id"])
        if order:
            return order.json()
        return {"message": "order not found!"}, 404

    def post(self):
        data = Order.fields.parse_args()
        order = OrderModel(**data)
        if OrderModel.find_order(order.id):
            return {"message": "order '{}' already exists!".format(order.id)}, 400
        elif not UserLoginServices.check_username(order.username):
            return {"message": "username '{}' not found!".format(order.username)}, 400
        else:
            try:
                order.save_order()
            except Exception:
                return {"message": "Internal Server Error!"}, 500
            return order.json()

    def put(self):
        data = Order.fields.parse_args()
        order_data = OrderModel.find_order(data["id"])
        if order_data:
            order_data.update_order(data["username"], data["item_id"], data["item_quantity"])
            order_data.save_order()
            return order_data.json(), 200
        order = OrderModel(**data)
        order.save_order()
        return order.json(), 201

    def delete(self):
        data = Order.fields.parse_args()
        order = OrderModel.find_order(data["id"])
        if order:
            try:
                order.delete_order()
            except:
                return {"message": "Internal Server Error!"}, 500
            return {"menssage": "order deleted!"}
        return {"menssage": "order not found or Password wrong!"}, 404
