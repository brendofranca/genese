from flask_restful import Resource, reqparse
from hermes_service.models.models import OrderModel


class Orders(Resource):
    def get(self):
        return {"Orders": [orders.json() for orders in OrderModel.query.all()]}


class Order(Resource):
    # TODO refatorar para que seja filtrado os argumentos nescessários em cada metodo.

    fields = reqparse.RequestParser()

    def get(self):
        Order.fields.add_argument("id", type=str, required=True, help="id is required!")
        Order.fields.remove_argument("username_id")
        Order.fields.remove_argument("item_id")
        Order.fields.remove_argument("item_quantity")
        data = Order.fields.parse_args()
        order = OrderModel.find_order(data["id"])
        if order:
            return order.json()
        return {"message": "order not found!"}, 404

    def post(self):
        Order.fields.add_argument("id", type=str, required=True, help="id is required!")
        Order.fields.add_argument("username_id", type=str, required=True, help="username_id is required!")
        Order.fields.add_argument("item_id", type=str, required=True, help="item_id is required!")
        Order.fields.add_argument("item_quantity", type=int, required=True, help="item_quantity is required!")
        data = Order.fields.parse_args()
        order = OrderModel(**data)
        if OrderModel.find_order(data["id"]):
            return {"message": "order '{}' already exists!".format(data["id"])}, 400
        try:
            order.save_order()
        except Exception:
            return {"message": "Internal Server Error!"}, 500
        return order.json()

    def put(self):
        Order.fields.add_argument("id", type=str, required=True, help="id is required!")
        Order.fields.add_argument("username_id", type=str, required=True, help="username_id is required!")
        Order.fields.add_argument("item_id", type=str, required=True, help="item_id is required!")
        Order.fields.add_argument("item_quantity", type=int, required=True, help="item_quantity is required!")
        data = Order.fields.parse_args()
        order_data = OrderModel.find_order(data["id"])
        if order_data:
            order_data.update_order(data["username_id"], data["item_id"], data["item_quantity"])
            order_data.save_order()
            return order_data.json(), 200
        order = OrderModel(**data)
        order.save_order()
        return order.json(), 201

    def delete(self):
        Order.fields.add_argument("id", type=str, required=True, help="id is required!")
        Order.fields.remove_argument("username_id")
        Order.fields.remove_argument("item_id")
        Order.fields.remove_argument("item_quantity")
        data = Order.fields.parse_args()
        order = OrderModel.find_order(data["id"])
        if order:
            try:
                order.delete_order()
            except:
                return {"message": "Internal Server Error!"}, 500
            return {"menssage": "order deleted!"}
        return {"menssage": "order not found or Password wrong!"}, 404
