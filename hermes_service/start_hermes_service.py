from flask import Flask
from flask_restful import Api
from Hermes_service.config.config import DevelopmentConfig
from Hermes_service.database.database import db
from Hermes_service.views.views import Orders, Order, OrderServiceCheckOrDelete

app = Flask(__name__)
api = Api(app)
app.config.from_object(DevelopmentConfig)


@app.before_first_request
def create_db():
    db.create_all()


api.add_resource(Orders, '/api/v1.0/orders/')  # endpoint for list all orders -> methods - [GET]
api.add_resource(OrderServiceCheckOrDelete, '/api/v1.0/order/<string:id>/')  # endpoint to check if exist a order or
# delete a order -> methods - [GET, DELETE]
api.add_resource(Order, '/api/v1.0/order/')  # endpoint to create and edit a order -> methods - [POST, PUT]

db.init_app(app)
app.run(port=8001)
