from flask import Flask
from flask_restful import Api
from jano_service.config.config import DevelopmentConfig
from jano_service.database.database import db
from jano_service.views.views import Users, User, UserServiceCheck, UserAuth

app = Flask(__name__)
api = Api(app)
app.config.from_object(DevelopmentConfig)


@app.before_first_request
def create_db():
    db.create_all()


api.add_resource(Users, '/api/v1.0/users/')  # endpoint for all users -> methods - [GET]
api.add_resource(UserAuth, '/api/v1.0/auth/')  # endpoint for authentication -> methods - [POST]
api.add_resource(User, '/api/v1.0/user/')  # endpoint for create, edit or delete a user -> methods - [POST, PUT, DELETE]
api.add_resource(UserServiceCheck, '/api/v1.0/user/<string:username>/')  # endpoint to check if user exist -> methods
# - [GET]

db.init_app(app)
app.run(port=8000)
