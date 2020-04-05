from flask import Flask
from flask_restful import Api
from hermes_service.config.config import DevelopmentConfig
from hermes_service.database.database import db
from hermes_service.views.views import Orders, Order

app = Flask(__name__)
api = Api(app)
app.config.from_object(DevelopmentConfig)


@app.before_first_request
def create_db():
    db.create_all()


api.add_resource(Orders, '/api/orders')
api.add_resource(Order, '/api/order')

db.init_app(app)
app.run()
