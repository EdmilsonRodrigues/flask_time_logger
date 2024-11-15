from datetime import datetime
from enum import Enum
from types import GenericAlias
from typing import Annotated, Union
from pydantic import BaseModel, Field
from flask_restx import fields


class BaseRequest(BaseModel):
    @classmethod
    def model(cls):
        data = {}
        model = (cls.__name__, data)
        for mro_class in cls.__mro__[:-1]:
            annotations = mro_class.__annotations__
            for key, annotation in annotations.items():
                key_type = annotation.__args__[0]
                metadata = annotation.__metadata__[0]
                description = metadata.description
                if isinstance(key_type, Annotated):
                    key_type = key_type.__args__[0]
                if isinstance(key_type, GenericAlias):
                    key_type = key_type.__origin__
                data[key] = cls.__get_fields_from_key_type(key_type, description)
                # print(key, annotation.__args__, annotation.__metadata__)
        print(model)
        return model

    @classmethod
    def __get_fields_from_key_type(cls, key_type, description: str):
        required = True
        if str(key_type).startswith("typing.Union[") and str(key_type).endswith("]"):
            description += "can be " " or ".join([str(arg) for arg in key_type.__args__])
            return fields.Raw(required=required, description=description)
        elif str(key_type).startswith("typing.Optional[") and str(key_type).endswith("]"):
            required = False
        elif key_type is list:
            return fields.List(fields.Raw, required=required, description=description)
        elif key_type is dict:
            return fields.Raw(required=required, description=description)
        elif key_type is tuple:
            return fields.List(fields.Raw, required=required, description=description)
        elif key_type is set:
            return fields.List(fields.Raw, required=required, description=description)
        elif key_type is int:
            return fields.Integer(required=required, description=description)
        elif key_type is str:
            return fields.String(required=required, description=description)
        elif key_type is float:
            return fields.Float(required=required, description=description)
        elif key_type is datetime:
            return fields.DateTime(required=required, description=description)
        elif issubclass(key_type, Enum):
            return fields.String(required=required, description=description)
        elif issubclass(key_type, BaseRequest):
            return fields.Nested(key_type.model())




class BaseClass(BaseRequest):
    id: Annotated[int, Field(description="The id of the object")]
    created_at: Annotated[datetime, Field(description="The date which the object was created")] = datetime.now()
    updated_at: Annotated[datetime, Field(description="The date which the object was last updated")] = datetime.now()

    @classmethod
    def table_name(cls) -> str:
        return cls.__name__.lower() + "s"

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
            elif isinstance(value, set):
                dump[key] = list(value)
        return dump


if __name__ == "__main__":
    print(BaseClass.model())
