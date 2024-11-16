from flask import request
from flask_restx import Namespace, Resource

from models.users import User, UserRequest


users_ns = Namespace("users", description="User related operations")


user_create_model = users_ns.model(UserRequest.model())

user_model = users_ns.model(User.model())


@users_ns.route("/")
class ListUsers(Resource):
    @users_ns.expect(user_create_model)
    @users_ns.marshal_with(user_model)
    def post(self):
        data = request.get_json()
        return data
