from flask import Flask
from flask_restful import Api
from jano_service.config.config import DevelopmentConfig
from jano_service.database.database import db
from jano_service.views.views import UsersLogins, UserLogin

app = Flask(__name__)
api = Api(app)
app.config.from_object(DevelopmentConfig)


@app.before_first_request
def create_db():
    db.create_all()


api.add_resource(UsersLogins, '/api/users')
api.add_resource(UserLogin, '/api/user/')

db.init_app(app)
app.run()
