from typing import Annotated
from pydantic import Field

from models.mixins import BaseClass, BaseRequest


class ProjectRequest(BaseRequest):
    name: Annotated[
        str,
        Field(
            description="The name of the project", database_field="name TEXT NOT NULL"
        ),
    ]
    description: Annotated[
        str,
        Field(
            description="The description of the project",
            database_field="description TEXT NOT NULL",
        ),
    ]
    department_id: Annotated[
        int,
        Field(
            description="The department id of the project",
            database_field="department_id INTEGER NOT NULL",
        ),
    ]
    estimated_hours: Annotated[
        int,
        Field(
            description="The estimated hours of the project",
            database_field="estimated_hours INTEGER NOT NULL",
        ),
    ]
    price_per_hour: Annotated[
        float,
        Field(
            description="The price per hour of the project",
            database_field="price_per_hour REAL NOT NULL",
        ),
    ]
    spent_hours: Annotated[
        int,
        Field(
            description="The spent hours of the project",
            database_field="spent_hours INTEGER NOT NULL",
        ),
    ] = 0
    user_ids: Annotated[
        list[int],
        Field(
            description="List of user IDs in the project",
            database_field="user_ids INTEGER[]",
        ),
    ] = []


class Project(BaseClass, ProjectRequest):
    pass
