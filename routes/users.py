from flask import request
from flask_restx import Namespace, Resource, fields
from dependencies import validated_dependency
from models.users import User, UserRequest


users_ns = Namespace("users", description="User related operations")


user_create_model = users_ns.model(UserRequest.model())
user_model = users_ns.model(User.model())
user_list_model = users_ns.model(
    "UsersList", {"users": fields.List(fields.Nested(user_model))}
)


@users_ns.route("/")
class ListUsers(Resource):
    @validated_dependency(
        namespace=users_ns,
        request_model=user_create_model,
        response_model=user_model,
        requires_authentication=False,
    )
    def post(self):
        user = User.create(UserRequest(**request.json))
        return user.json(), 201

    @validated_dependency(namespace=users_ns, response_model=user_model)
    def get(self):
        users = User.list_all()
        return {"users": [user.json() for user in users]}, 200


@users_ns.route("/<int:id>")
class UserResource(Resource):
    @validated_dependency(namespace=users_ns, response_model=user_model)
    def get(self, id):
        user = User.get(id)
        return user.json(), 200

    @validated_dependency(
        namespace=users_ns, request_model=user_create_model, response_model=user_model
    )
    def put(self, id):
        user = User.get(id).json()
        updated_user = UserRequest(**request.json).model_dump()
        user.update(updated_user)
        user = User(**user)
        user = user.save()
        return user.json(), 200

    @validated_dependency(namespace=users_ns)
    def delete(self, id):
        user = User.get(id)
        user.delete()
        return {"message": "User deleted"}, 200
