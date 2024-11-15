from datetime import datetime
from pydantic import BaseModel
from models.mixins import BaseClass


class TimeLogRequest(BaseModel):
    user_id: int
    project_id: int
    time_in: datetime
    time_out: datetime


class TimeLog(BaseClass, BaseModel):
    pass
