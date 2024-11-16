from typing import Annotated, Optional
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
        Optional[str],
        Field(
            description="The password of the user",
            database_field="password TEXT NOT NULL",
        ),
    ] = None
    department: Annotated[
        str,
        Field(
            description="The department of the user",
            database_field="department TEXT NOT NULL",
        ),
    ] = "all"
    role: Annotated[
        str,
        Field(description="The role of the user", database_field="role TEXT NOT NULL"),
    ] = "admin"


class User(BaseClass, UserRequest):
    def encrypt_password(self) -> str:
        password = self.password + SECRET_KEY
        sha256_password = sha256(password.encode()).hexdigest()
        return sha256_password

    def json(self, exclude_password: bool = False) -> dict:
        dump = super().json()
        if not exclude_password:
            dump["password"] = self.encrypt_password()
        else:
            dump.pop("password", None)
        return dump
    
    def save(self) -> BaseClass:
        return super().save(exclude_password=True)

    @classmethod
    def get_by_email(cls, email) -> "User":
        return cls.get_by_field("email", email)

    def validate_password(self, password: str) -> bool:
        original = self.password
        self.password = password
        return self.encrypt_password() == original

    @property
    def is_admin(self) -> bool:
        return self.role.lower() == "admin"


class UserResponse(User):
    def json(self) -> dict:
        dump = super().json(exclude_password=True)
        dump.pop("password", None)
        return dump


if __name__ == "__main__":
    print(User.create_table())
