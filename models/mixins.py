from collections.abc import Generator
from datetime import datetime
from enum import Enum
from types import GenericAlias
from typing import Annotated, Any
from pydantic import BaseModel, Field
from flask_restx import fields
from session import db


class BaseRequest(BaseModel):
    @classmethod
    def model(cls) -> tuple[str | dict]:
        data = {}
        model = (cls.__name__, data)
        for key, annotation in cls.get_annotations():
            key_type = annotation.__args__[0]
            metadata = annotation.__metadata__[0]
            description = metadata.description
            if isinstance(key_type, Annotated):
                key_type = key_type.__args__[0]
            if isinstance(key_type, GenericAlias):
                key_type = key_type.__origin__
            data[key] = cls.__get_fields_from_key_type(key_type, description)
            # print(key, annotation.__args__, annotation.__metadata__)
        return model

    @classmethod
    def get_annotations(cls) -> Generator[tuple, None, None]:
        for mro_class in cls.mro()[:-1]:
            for key, annotation in mro_class.__annotations__.items():
                yield key, annotation

    @classmethod
    def __get_fields_from_key_type(cls, key_type, description: str) -> fields.Raw:
        required = True
        if str(key_type).startswith("typing.Union[") and str(key_type).endswith("]"):
            description += "can be " " or ".join(
                [str(arg) for arg in key_type.__args__]
            )
            return fields.Raw(required=required, description=description)
        elif str(key_type).startswith("typing.Optional[") and str(key_type).endswith(
            "]"
        ):
            key_type = key_type.__args__[0]
            required = False
        if key_type is list:
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
    id: Annotated[
        int,
        Field(
            description="The id of the object",
            database_field="id INTEGER PRIMARY KEY AUTOINCREMENT",
        ),
    ]
    created_at: Annotated[
        datetime,
        Field(
            description="The date which the object was created",
            database_field="created_at TEXT NOT NULL",
        ),
    ] = datetime.now()
    updated_at: Annotated[
        datetime,
        Field(
            description="The date which the object was last updated",
            database_field="updated_at TEXT NOT NULL",
        ),
    ] = datetime.now()

    @classmethod
    def table_name(cls) -> str:
        return cls.__name__.lower() + "s"

    @classmethod
    def list_all(cls) -> list:
        return db.list_all(cls)

    @classmethod
    def get(cls, id) -> "BaseClass":
        return db.get(cls, id)

    @classmethod
    def get_by_field(cls, field: str, value: Any) -> "BaseClass":
        return db.get_by_field(cls, field, value)

    def save(self, exclude_password: bool = False) -> "BaseClass":
        self.updated_at = datetime.now()
        return db.update(self, exclude_password=exclude_password)

    def delete(self) -> bool:
        return db.delete(self)

    @classmethod
    def create(cls, request: BaseRequest) -> "BaseClass":
        self = cls(**request.model_dump(), id=-100)
        return db.create(self)

    def json(self) -> dict:
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

    @classmethod
    def create_table(cls) -> str:
        command = f"CREATE TABLE IF NOT EXISTS {cls.table_name()} (\n"
        for _, annotation in cls.get_annotations():
            metadata = annotation.__metadata__[0]
            command += f"\t{metadata.json_schema_extra['database_field']},\n"
        command = command[:-2] + "\n"
        command += ")"
        return command


if __name__ == "__main__":
    print(BaseClass.create_table())
