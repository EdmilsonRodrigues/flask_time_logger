from flask import request
from flask_restx import Namespace, Resource
from routes.dependencies import validated_dependency
from models.users import User, UserRequest
from routes.users import user_create_model, user_list_model, user_model


admin_ns = Namespace("admin", description="Admin only operations")


@admin_ns.route("/users")
class ListUsers(Resource):
    @validated_dependency(
        namespace=admin_ns, response_model=user_list_model, requires_admin=True
    )
    def get(self):
        users = User.list_all()
        return {"results": [user.json() for user in users]}, 200


@admin_ns.route("/users/<int:id>")
class UserResource(Resource):
    @validated_dependency(
        namespace=admin_ns, response_model=user_model, requires_admin=True
    )
    def get(self, id):
        user = User.get(id)
        return user.json(), 200

    @validated_dependency(
        namespace=admin_ns,
        request_model=user_create_model,
        response_model=user_model,
        requires_admin=True,
    )
    def put(self, id):
        user = User.get(id).json()
        updated_user = UserRequest(**request.json).model_dump()
        user.update(updated_user)
        user = User(**user)
        user = user.save()
        return user.json(), 200

    @validated_dependency(namespace=admin_ns, requires_admin=True)
    def delete(self, id):
        user = User.get(id)
        user.delete()
        return {"message": "User deleted"}, 200
