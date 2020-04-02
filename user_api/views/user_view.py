from flask_restful import Resource, reqparse
from user_api.models.user_model import UserModel


class Users(Resource):
    def get(self):
        return {"Users": [users.json() for users in UserModel.query.all()]}


class User(Resource):
    fields = reqparse.RequestParser()
    fields.add_argument("name", type=str, required=True, help="NAME is required!")
    fields.add_argument("cpf", type=int, required=True, help="CPF is required!")
    fields.add_argument("email", type=str)
    fields.add_argument("phone_number", type=int)

    def get(self, id):
        user = UserModel.find_user(id)

        if user:
            return user.json()
        return {"message": "User not found!"}, 404

    def post(self, id):

        if UserModel.find_user(id):
            return {"message": "ID '{}' already exists!".format(id)}, 400

        data = User.fields.parse_args()
        user = UserModel(id, **data)

        try:
            user.save_user()
        except Exception:
            return {"message": "Internal Server Error!"}, 500
        return user.json()

    def put(self, id):
        data = User.fields.parse_args()
        user_data = UserModel.find_user(id)

        if user_data:
            user_data.update_user(**data)
            user_data.save_user()
            return user_data.json(), 200

        user = UserModel(id, **data)
        user.save_user()
        return user.json(), 201

    def delete(self, id):
        user = UserModel.find_user(id)

        if user:
            try:
                user.delete_user()
            except:
                return {"message": "Internal Server Error!"}, 500
            return {"menssage": "User deleted!"}
        return {"menssage": "User not found!"}, 404
