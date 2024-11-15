from pydantic import BaseModel

from models.mixins import BaseClass


class DepartmentRequest(BaseModel):
    name: str
    description: str
    users: list[int] = []
    admins: list[int] = []


class Department(BaseClass, DepartmentRequest):
    pass
