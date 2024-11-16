from flask import request
import functools
from typing import Callable
from models.users import User
from services.auth import Auth
from flask_restx import Model, Namespace, OrderedModel


def get_session_from_header() -> User | None:
    # Get the Authorization header
    auth_header = request.headers.get("Authorization")

    if auth_header is None:
        return {"message": "Missing Authorization header"}, 401

    # Extract the token (assumes the format is "Bearer <token>")
    token = auth_header.split(" ")[1] if " " in auth_header else None

    if auth_header.split(" ")[0] != "Bearer" or token is None:
        return {"message": "Invalid token format"}, 401

    return Auth.decode_jwt(token)


def session_dependency(function: Callable, return_session: bool) -> Callable:
    @functools.wraps(function)
    def decorated_function(*args, **kwargs) -> Callable:
        session = get_session_from_header()

        if isinstance(session, tuple):
            return session

        if session is None:
            return {"message": "Invalid token"}, 401

        if return_session:
            kwargs["session"] = User.get(session["user_id"])

        return function(*args, **kwargs)

    return decorated_function


def admin_dependency(function: Callable, return_session: bool) -> Callable:
    @functools.wraps(function)
    def decorated_function(*args, **kwargs):
        session = get_session_from_header()

        if session is None:
            return {"message": "Invalid token"}, 401

        session: User = User.get(session["user_id"])

        if not session.is_admin:
            return {"message": "Unauthorized"}, 403

        if return_session:
            kwargs["session"] = session

        return function(*args, **kwargs)

    return decorated_function


def validated_dependency(
    namespace: Namespace,
    response_model: Model | OrderedModel | None = None,
    request_model: Model | OrderedModel | None = None,
    requires_authentication: bool = True,
    requires_admin: bool = False,
    return_session: bool = False,
) -> Callable:
    def decorator(function: Callable) -> Callable:
        try:
            @functools.wraps(function)
            def decorated_function(*args, **kwargs):
                if requires_admin:
                    return admin_dependency(function, return_session=return_session)(
                        *args, **kwargs
                    )
                if requires_authentication:
                    return session_dependency(function, return_session=return_session)(
                        *args, **kwargs
                    )
                return function(*args, **kwargs)

            if requires_authentication:
                decorated_function = namespace.doc(security="bearerAuth")(
                    decorated_function
                )

            if request_model is not None:
                decorated_function = namespace.expect(request_model, validate=True)(
                    decorated_function
                )

            if response_model is not None:
                decorated_function = namespace.marshal_with(response_model)(
                    decorated_function
                )
            return decorated_function
        except Exception as e:
            print(e)
            raise

    return decorator
