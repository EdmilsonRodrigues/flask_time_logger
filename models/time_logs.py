from datetime import datetime
from models.mixins import BaseClass, BaseRequest
from typing import Annotated, Optional
from pydantic import Field


class TimeLogRequest(BaseRequest):
    user_id: Annotated[
        int,
        Field(
            description="The ID of the user", database_field="user_id INTEGER NOT NULL"
        ),
    ]
    project_id: Annotated[
        Optional[int],
        Field(
            description="The ID of the project",
            database_field="project_id INTEGER",
        ),
    ] = None
    time_in: Annotated[
        datetime,
        Field(
            description="The time the user logged in",
            database_field="time_in TEXT NOT NULL",
        ),
    ] = datetime.now()
    time_out: Annotated[
        Optional[datetime],
        Field(
            description="The time the user logged out",
            database_field="time_out TEXT",
        ),
    ] = None


class TimeLog(BaseClass, TimeLogRequest):
    @classmethod
    def start(cls, user_id: int, project_id: int | None = None) -> "TimeLog":
        time_log = TimeLogRequest(
            user_id=user_id, project_id=project_id, time_in=datetime.now()
        )
        return TimeLog.create(time_log)

    @classmethod
    def stop(cls, user_id: int) -> "TimeLog":
        time_log = TimeLog.get_running(user_id)
        time_log.time_out = datetime.now()
        return time_log.save()

    @classmethod
    def get_running(cls, user_id: int) -> "TimeLog":
        return TimeLog.get_by_fields({"user_id": user_id, "time_out": None})
