from flask import Flask
from flask_restful import Api
from user_api.views.user_view import Users, User
from config.user_api_config import DevelopmentConfig

user_app = Flask(__name__)
user_api = Api(user_app)
user_app.config.from_object(DevelopmentConfig)


@user_app.before_first_request
def create_database():
    database.create_all()


user_api.add_resource(Users, '/api/users')
user_api.add_resource(User, '/api/user/<int:id>')

if __name__ == '__main__':
    from user_api.db.user_database import user_database as database
    database.init_app(user_app)
    user_app.run(host='127.0.1.1', port=5000, debug=True)
