from flask_restful import Resource, reqparse
from jano_service.models.models import UserModel
from jano_service.tools.extras import check_password


class Users(Resource):
    # returns all users in a json document
    def get(self):
        return {"Users": [users.json() for users in UserModel.query.all()]}


class User(Resource):
    fields = reqparse.RequestParser()
    fields.add_argument("username", type=str, required=True, help="username is required!")
    fields.add_argument("password", type=str, required=True, help="password is required!")

    # to create a new user
    def post(self):
        data = User.fields.parse_args()
        user = UserModel(**data)
        if UserModel.find_user_login(data["username"]):
            return {"message": "username '{}' already exists!".format(data["username"])}, 400
        try:
            user.save_user_login(data["password"])
        except Exception:
            return {"message": "Internal Server Error!"}, 500
        return user.json()

    # to edit a user or create if nt exists in db
    def put(self):
        data = User.fields.parse_args()
        user_data = UserModel.find_user_login(data["username"])
        if user_data:
            user_data.update_user_login(**data)
            user_data.save_user_login(data["password"])
            return user_data.json(), 200

        user = UserModel(**data)
        user.save_user_login(data["password"])
        return user.json(), 201

    # to delete a user
    def delete(self):
        data = User.fields.parse_args()
        user = UserModel.find_user_login(data["username"])
        if user and check_password(user.password, data["password"]):
            try:
                user.delete_user_login()
            except:
                return {"message": "Internal Server Error!"}, 500
            return {"menssage": "username deleted!"}
        return {"menssage": "username not found or Password wrong!"}, 404


class UserServiceCheck(Resource):
    fields = reqparse.RequestParser()
    fields.add_argument("username", type=str, required=True, help="username is required!")

    # just check if user exist and returns info
    def get(self, username):
        user = UserModel.find_user_login(username)
        if user:
            return user.json()
        return {"message": "username not found!"}, 404


class UserAuth(Resource):
    fields = reqparse.RequestParser()
    fields.add_argument("username", type=str, required=True, help="username is required!")
    fields.add_argument("password", type=str, required=True, help="password is required!")

    # TODO: I have study and implemented new forms to do this.
    # serves to auth, its just temporary function
    def post(self):
        data = User.fields.parse_args()
        user = UserModel.find_user_login(data["username"])
        if user and check_password(user.password, data["password"]):
            return user.json()
        return {"message": "username not found or password wrong!"}, 404
