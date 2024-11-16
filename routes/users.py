from flask import request
from flask_restx import Namespace, Resource, fields
from routes.dependencies import validated_dependency
from models.users import User, UserRequest, UserResponse


users_ns = Namespace("users", description="User related operations")


user_create_model = users_ns.model(*UserRequest.model())
user_model = users_ns.model(*UserResponse.model())
user_list_model = users_ns.model(
    "UsersList", {"results": fields.List(fields.Nested(user_model))}
)


@users_ns.route("/")
class CreateUsers(Resource):
    @validated_dependency(
        namespace=users_ns,
        request_model=user_create_model,
        response_model=user_model,
        requires_authentication=False,
    )
    def post(self):
        user = User.create(UserRequest(**request.json))
        return user.json(), 201


@users_ns.route("/me")
class MeResource(Resource):
    @validated_dependency(
        namespace=users_ns, response_model=user_model, return_session=True
    )
    def get(self, session: User):
        return UserResponse(**session.model_dump()).json(), 200

    @validated_dependency(
        namespace=users_ns,
        request_model=user_create_model,
        response_model=user_model,
        return_session=True,
    )
    def put(self, session: User):
        user = session.json()
        updated_user = UserRequest(**request.json)
        user.update(updated_user)
        user = User(**user)
        user = user.save()
        return UserResponse(**user.model_dump()).json(), 200

    @validated_dependency(namespace=users_ns, return_session=True)
    def delete(self, session: User):
        session.delete()
        return {"message": "User deleted"}, 200
