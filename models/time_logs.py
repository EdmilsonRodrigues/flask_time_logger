from datetime import datetime
from models.mixins import BaseClass, BaseRequest
from typing import Annotated
from pydantic import Field


class TimeLogRequest(BaseRequest):
    user_id: Annotated[
        int,
        Field(
            description="The ID of the user", database_field="user_id INTEGER NOT NULL"
        ),
    ]
    project_id: Annotated[
        int,
        Field(
            description="The ID of the project",
            database_field="project_id INTEGER NOT NULL",
        ),
    ]
    time_in: Annotated[
        datetime,
        Field(
            description="The time the user logged in",
            database_field="time_in TIMESTAMP NOT NULL",
        ),
    ]
    time_out: Annotated[
        datetime,
        Field(
            description="The time the user logged out",
            database_field="time_out TIMESTAMP NOT NULL",
        ),
    ]


class TimeLog(BaseClass, TimeLogRequest):
    pass
