from datetime import datetime
from enum import Enum
from pydantic import BaseModel


class BaseClass(BaseModel):
    id: int
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()

    def save(self):
        self.updated_at = datetime.now()
        # Logic to save to database
        return self
    
    def delete(self):
        # Logic to delete from database
        return True

    def create(self):
        # Logic to create in database
        return self
    
    def json(self):
        dump = self.model_dump()
        for key, value in dump.items():
            if isinstance(value, datetime):
                dump[key] = value.isoformat()
            elif isinstance(value, BaseClass):
                dump[key] = value.json()
            elif isinstance(value, Enum):
                dump[key] = value.value
        return dump    
