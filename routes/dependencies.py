from flask import request
import functools
from typing import Callable

from models.users import User
from services.auth import Auth
from flask_restx import Model, Namespace, OrderedModel


def session_dependency(function: Callable) -> Callable:
    @functools.wraps(function)
    def decorated_function(*args, **kwargs):
        # Get the Authorization header
        auth_header = request.headers.get("Authorization")

        if auth_header is None:
            return {"message": "Missing Authorization header"}, 401

        # Extract the token (assumes the format is "Bearer <token>")
        token = auth_header.split(" ")[1] if " " in auth_header else None

        session = Auth.decode_jwt(token)

        if session is None:
            return {"message": "Invalid token"}, 401

        kwargs["session"] = User.get(session["user_id"])

        return function(*args, **kwargs)

    return decorated_function


def validated_dependency(
    function: Callable,
    namespace: Namespace,
    request_model: Model | OrderedModel,
    response_model: Model | OrderedModel,
    requires_authentication: bool = False,
) -> Callable:
    @functools.wraps(function)
    @namespace.expect(request_model, validate=True)
    @namespace.marshal_with(response_model)
    def decorated_function(*args, **kwargs):
        if requires_authentication:
            return session_dependency(function)(*args, **kwargs)
        return function(*args, **kwargs)

    return decorated_function
