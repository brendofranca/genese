from flask_restful import Resource, reqparse
from jano_service.models.models import UserLoginModel
from jano_service.tools.extras import check_password


class UsersLogins(Resource):
    def get(self):
        return {"UsersLogins": [users.json() for users in UserLoginModel.query.all()]}


class UserLogin(Resource):
    fields = reqparse.RequestParser()
    fields.add_argument("username", type=str, required=True, help="username is required!")
    fields.add_argument("password", type=str, required=True, help="password is required!")

    def get(self):

        data = UserLogin.fields.remove_argument("password").parse_args()
        user = UserLoginModel.find_user_login(data["username"])

        if user:
            return user.json()
        return {"message": "username not found!"}, 404

    def post(self):

        data = UserLogin.fields.add_argument("password").parse_args()
        user = UserLoginModel(**data)

        if UserLoginModel.find_user_login(data["username"]):
            return {"message": "username '{}' already exists!".format(data["username"])}, 400

        try:
            user.save_user_login(data["password"])
        except Exception:
            return {"message": "Internal Server Error!"}, 500
        return user.json()

    def put(self):

        data = UserLogin.fields.parse_args()
        user_data = UserLoginModel.find_user_login(data["username"])

        if user_data:
            user_data.update_user_login(**data)
            user_data.save_user_login(data["password"])
            return user_data.json(), 200

        user = UserLoginModel(**data)
        user.save_user_login(data["password"])
        return user.json(), 201

    def delete(self):

        data = UserLogin.fields.parse_args()
        user = UserLoginModel.find_user_login(data["username"])

        if user and check_password(user.password, data["password"]):
            try:
                user.delete_user_login()
            except:
                return {"message": "Internal Server Error!"}, 500
            return {"menssage": "username deleted!"}
        return {"menssage": "username not found or Password wrong!"}, 404
