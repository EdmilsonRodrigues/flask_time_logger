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
    user_ids: Annotated[
        list[int],
        Field(
            description="List of user IDs in the department",
            database_field="user_ids INTEGER[]",
        ),
    ] = []
    admin_ids: Annotated[
        list[int],
        Field(
            description="List of admin IDs in the department",
            database_field="admin_ids INTEGER[]",
        ),
    ] = []


class Department(BaseClass, DepartmentRequest):
    pass


if __name__ == "__main__":
    print(DepartmentRequest.model())
