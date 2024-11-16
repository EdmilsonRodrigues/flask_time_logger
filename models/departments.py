from models.mixins import BaseClass, BaseRequest
from typing import Annotated
from pydantic import Field


class DepartmentRequest(BaseRequest):
    name: Annotated[
        str,
        Field(
            description="The name of the department",
            database_field="name TEXT NOT NULL",
        ),
    ]
    description: Annotated[
        str,
        Field(
            description="The description of the department",
            database_field="description TEXT NOT NULL",
        ),
    ]
    users: Annotated[
        list[int],
        Field(
            description="List of user IDs in the department",
            database_field="users INTEGER[]",
        ),
    ] = []
    admins: Annotated[
        list[int],
        Field(
            description="List of admin IDs in the department",
            database_field="admins INTEGER[]",
        ),
    ] = []


class Department(BaseClass, DepartmentRequest):
    pass


if __name__ == "__main__":
    print(DepartmentRequest.model())
