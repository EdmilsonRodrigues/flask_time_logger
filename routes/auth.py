from flask import request
from flask_restx import Namespace, Resource, fields
from models.users import User
from services.auth import Auth


auth_ns = Namespace("auth", description="Authentication related operations")


# Request model for form-data
auth_request = auth_ns.model(
    "AuthRequest",
    {
        "username": fields.String(required=True, description="The email of the user"),
        "password": fields.String(
            required=True, description="The password of the user"
        ),
    },
)

# Response model
auth_response = auth_ns.model(
    "AuthResponse",
    {
        "access_token": fields.String(required=True, description="The access token"),
        "token_type": fields.String(
            required=True,
            description="The type of token, e.g., bearer",
            default="bearer",
        ),
    },
)


@auth_ns.route("/login")
class LoginResource(Resource):
    @auth_ns.expect(auth_request, validate=True)
    @auth_ns.marshal_with(
        auth_response, code=200, description="Successfully authenticated"
    )
    def post(self):
        """
        Authenticate user and return an access token.
        """
        # Extract form data
        email = request.json["username"]
        password = request.json["password"]

        user = User.get_by_email(email)
        if user.validate_password(password):
            # Mock access token (In production, use libraries like PyJWT to generate real tokens)
            access_token = Auth.gen_jwt(user)
            return {"access_token": access_token, "token_type": "bearer"}, 200

        # Invalid credentials
        auth_ns.abort(401, "Invalid username or password")
