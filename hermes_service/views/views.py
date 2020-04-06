from flask_restful import Resource, reqparse
from Hermes_service.models.models import OrderModel, UserLoginServices


class Orders(Resource):
    # returns all orders in a json document
    def get(self):
        return {"Orders": [orders.json() for orders in OrderModel.query.all()]}


class Order(Resource):
    fields = reqparse.RequestParser()
    fields.add_argument("id", type=str, required=True, help="id is required!")
    fields.add_argument("username_id", type=str, required=True, help="username_id is required!")
    fields.add_argument("item_id", type=str, required=True, help="item_id is required!")
    fields.add_argument("item_quantity", type=int, required=True, help="item_quantity is required!")

    # to create a new order
    def post(self):
        data = Order.fields.parse_args()
        order = OrderModel(**data)
        if OrderModel.find_order(order.id):
            return {"message": "order '{}' already exists!".format(order.id)}, 400
        elif not UserLoginServices.check_username(order.username_id):
            return {"message": "username_id '{}' not found!".format(order.username_id)}, 400
        else:
            try:
                order.save_order()
            except Exception:
                return {"message": "Internal Server Error!"}, 500
            return order.json()

    # to edit order or create a new if not exist
    def put(self):
        data = Order.fields.parse_args()
        order = OrderModel(**data)
        order_data = OrderModel.find_order(data["id"])
        if order_data and UserLoginServices.check_username(order.username_id):
            order_data.update_order(data["username_id"], data["item_id"], data["item_quantity"])
            order_data.save_order()
            return order_data.json(), 200
        elif not UserLoginServices.check_username(order.username_id):
            return {"message": "username_id '{}' not found!".format(order.username_id)}, 400
        else:
            order.save_order()
            return order.json(), 201


class OrderServiceCheckOrDelete(Resource):

    # just check if order exist and returns info
    def get(self, id):
        order = OrderModel.find_order(id)
        if order:
            return order.json()
        return {"message": "order not found!"}, 404

    # to delete order
    def delete(self, id):
        order = OrderModel.find_order(id)
        if order:
            try:
                order.delete_order()
            except:
                return {"message": "Internal Server Error!"}, 500
            return {"menssage": "order deleted!"}
        return {"menssage": "order not found!"}, 404
