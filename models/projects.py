from pydantic import BaseModel

from models.mixins import BaseClass


class ProjectRequest(BaseModel):
    name: str
    description: str
    department_id: int
    estimated_hours: int
    price_per_hour: float


class Project(BaseClass, ProjectRequest):
    pass
