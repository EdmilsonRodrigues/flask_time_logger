from pydantic import BaseModel
from config import SECRET_KEY
from models.mixins import BaseClass
from hashlib import sha256


class UserRequest(BaseModel):
    name: str
    email: str
    password: str
    department: str
    role: str


class User(BaseClass, UserRequest):
    def encrypt_password(self):
        password = self.password + SECRET_KEY
        sha256_password = sha256(password.encode()).hexdigest()
        return sha256_password
    
    def json(self):
        dump = super().json()
        dump["password"] = self.encrypt_password()
    
    def validate_password(self, password):
        return self.encrypt_password() == password


class UserResponse(User):
    def json(self):
        dump = super().json()
        dump.pop('password')
        return dump
