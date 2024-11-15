from typing import Annotated
from pydantic import BaseModel, Field
from config import SECRET_KEY
from models.mixins import BaseClass
from hashlib import sha256


class UserRequest(BaseModel):
    name: Annotated[str, Field(description="The name of the user", database_field="name TEXT NOT NULL")]
    email: Annotated[str, Field(description="The email of the user", database_field="email TEXT NOT NULL")]
    password: Annotated[str, Field(description="The password of the user", database_field="password TEXT NOT NULL")]
    department: Annotated[str, Field(description="The department of the user", database_field="department TEXT NOT NULL")]
    role: Annotated[str, Field(description="The role of the user", database_field="role TEXT NOT NULL")]


class User(BaseClass, UserRequest):
    def encrypt_password(self):
        password = self.password + SECRET_KEY
        sha256_password = sha256(password.encode()).hexdigest()
        return sha256_password

    def json(self):
        dump = super().json()
        dump["password"] = self.encrypt_password()
        return dump

    def validate_password(self, password):
        return self.encrypt_password() == password


class UserResponse(User):
    def json(self):
        dump = super().json()
        dump.pop("password")
        return dump


if __name__ == "__main__":
    print(User.create_table())
