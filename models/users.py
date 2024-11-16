from typing import Annotated
from pydantic import Field
from config import SECRET_KEY
from models.mixins import BaseClass, BaseRequest
from hashlib import sha256


class UserRequest(BaseRequest):
    name: Annotated[
        str,
        Field(description="The name of the user", database_field="name TEXT NOT NULL"),
    ]
    email: Annotated[
        str,
        Field(
            description="The email of the user", database_field="email TEXT NOT NULL"
        ),
    ]
    password: Annotated[
        str,
        Field(
            description="The password of the user",
            database_field="password TEXT NOT NULL",
        ),
    ]
    department: Annotated[
        str,
        Field(
            description="The department of the user",
            database_field="department TEXT NOT NULL",
        ),
    ]
    role: Annotated[
        str,
        Field(description="The role of the user", database_field="role TEXT NOT NULL"),
    ]


class User(BaseClass, UserRequest):
    def encrypt_password(self) -> str:
        password = self.password + SECRET_KEY
        sha256_password = sha256(password.encode()).hexdigest()
        return sha256_password

    def json(self) -> dict:
        dump = super().json()
        dump["password"] = self.encrypt_password()
        return dump

    @classmethod
    def get_by_email(cls, email) -> "User":
        return cls.get_by_field("email", email)

    def validate_password(self, password: str) -> bool:
        return self.encrypt_password() == password


class UserResponse(User):
    def json(self) -> dict:
        dump = super().json()
        dump.pop("password")
        return dump


if __name__ == "__main__":
    print(User.create_table())
