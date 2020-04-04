from flask import Flask
from flask_restful import Api
from jano_service.config import DevelopmentConfig
from jano_service.database import db
from jano_service.views import UsersLogins, UserLogin

jano_app = Flask(__name__)
jano_api = Api(jano_app)
jano_app.config.from_object(DevelopmentConfig)


@jano_app.before_first_request
def create_db():
    db.create_all()


jano_api.add_resource(UsersLogins, '/api/users')
jano_api.add_resource(UserLogin, '/api/user/')

db.init_app(jano_app)
jano_app.run()
