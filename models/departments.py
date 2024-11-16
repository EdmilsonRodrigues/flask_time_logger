from pydantic import BaseModel

from models.mixins import BaseClass
from typing import Annotated
from pydantic import Field


class DepartmentRequest(BaseModel):
    name: Annotated[str, Field(description="The name of the department", database_field="name TEXT NOT NULL")]
    description: Annotated[str, Field(description="The description of the department", database_field="description TEXT NOT NULL")]
    users: Annotated[list[int], Field(description="List of user IDs in the department", database_field="users INTEGER[]")] = []
    admins: Annotated[list[int], Field(description="List of admin IDs in the department", database_field="admins INTEGER[]")] = []


class Department(BaseClass, DepartmentRequest):
    pass
