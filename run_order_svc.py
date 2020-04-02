from flask import Flask
from flask_restful import Api
from order_api.views.order_view import Orders, Order
from config.user_api_config import DevelopmentConfig

order_app = Flask(__name__)
order_api = Api(order_app)
order_app.config.from_object(DevelopmentConfig)


@order_app.before_first_request
def create_database():
    database.create_all()


order_api.add_resource(Orders, '/api/orders')
order_api.add_resource(Order, '/api/order/<int:id>')

if __name__ == '__main__':
    from order_api.db.order_database import order_database as database

    database.init_app(order_app)
    order_app.run(host='127.0.1.1', port=5005, debug=True)
