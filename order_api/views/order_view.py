from flask_restful import Resource, reqparse
from order_api.models.order_model import OrderModel, UserService


class Orders(Resource):
    def get(self):
        return {"Orders": [orders.json() for orders in OrderModel.query.all()]}


class Order(Resource):
    fields = reqparse.RequestParser()
    fields.add_argument("user_id", type=int, required=True, help="USER_ID is required!")
    fields.add_argument("item_description", type=str, required=True, help="ITEM_DESCRIPTION is required!")
    fields.add_argument("item_quantity", type=int, required=True, help="ITEM_QUANTITY is required!")
    fields.add_argument("item_price", type=float, required=True, help="ITEM_PRICE is required!")

    def get(self, id):
        order = OrderModel.find_order(id)

        if order:
            return order.json()
        return {"message": "Order not found!"}

    def post(self, id):
        if OrderModel.find_order(id):
            return {"message": "ID '{}' already exists!".format(id)}, 400

        data = Order.fields.parse_args()
        order = OrderModel(id, **data)
        user_sts = UserService.get_user(order.user_id)

        if user_sts:
            try:
                order.save_order()
            except Exception:
                return {"message": "Internal Server Erro!"}, 500
            return order.json()
        else:
            return {"message": "USER_ID '{}' not found!".format(order.user_id)}, 404

    def put(self, id):
        data = Order.fields.parse_args()
        order_data = OrderModel.find_order(id)

        if order_data:
            order_data.update_order(**data)
            user_sts = UserService.get_user(order_data.user_id)
            if user_sts:
                try:
                    order_data.save_order()
                except:
                    return {"message": "Internal Server Erro!"}, 500
                return order_data.json(), 200
            else:
                return {"message": "USER_ID '{}' not found!".format(order_data.user_id)}, 404

        order = OrderModel(id, **data)
        user_sts = UserService.get_user(order.user_id)

        if user_sts:
            try:
                order.save_order()
            except:
                return {"message": "Internal Server Erro!"}, 500
            return order.json(), 201
        else:
            return {"message": "USER_ID '{}' not found!".format(order.user_id)}, 404

    def delete(self, id):
        order = OrderModel.find_order(id)

        if order:
            try:
                order.delete_order()
            except:
                return {"message": "Internal Server Error!"}, 500
            return {"menssage": "Order deleted!"}
        return {"menssage": "Order not found!"}, 404
