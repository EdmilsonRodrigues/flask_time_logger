from typing import Any, Callable

# from models.mixins import BaseClass


class Database:
    def __init__(self, get_db: Callable):
        self.get_db = get_db

    def get_schema(self, model: type, dml: bool = False):
        with self.get_db() as conn:
            cursor = conn.cursor()
            cursor.execute(f"PRAGMA table_info({model.table_name()})")
            shcema = {}
            for row in cursor.fetchall():
                if dml:
                    if row[1] == "id":
                        continue
                    shcema[row[0] - 1] = row[
                        1
                    ]  # removed the index since it's not needed to create nor update
                else:
                    shcema[row[0]] = row[1]
            return shcema

    def _gen_object(self, model: type, fields: tuple):
        schema = self.get_schema(model)
        mapping = {schema[index]: fields[index] for index in range(len(fields))}
        return model(**mapping)

    def _gen_insert_query(
        self,
        model: type,
        model_instance,
        id: int | None = None,
        exclude_password: bool = False,
    ):
        schema = self.get_schema(model, dml=True)
        dump = model_instance.json(exclude_password=exclude_password)
        print(schema)
        print(dump)
        columns = ", ".join(schema.values())
        placeholders = ", ".join("?" * len(schema))
        values = list("$placeholder" for _ in range(len(schema)))
        items = schema.items()
        for index, key in tuple(items):
            if exclude_password and key == "password":
                schema.pop(index)
                continue
            values[index] = dump[key]
        while "$placeholder" in values:
            values.remove("$placeholder")
        if id is not None:
            set_clause = ", ".join([f"{col} = ?" for col in schema.values()])
            values.append(id)
            return f"UPDATE {model.table_name()} SET {set_clause} WHERE id = ?", tuple(
                values
            )
        return (
            f"INSERT INTO {model.table_name()} ({columns}) VALUES ({placeholders})",
            tuple(values),
        )

    def list_all(
        self, model: type, user_id: int | None = None, user_ids: int | None = None
    ):
        with self.get_db() as conn:
            cursor = conn.cursor()
            if user_id is not None:
                cursor.execute(
                    f"SELECT * FROM {model.table_name()} WHERE user_id=?", (user_id,)
                )
            elif user_ids is not None:
                cursor.execute(
                    f"SELECT * FROM {model.table_name()} WHERE EXISTS (SELECT 1 FROM json_each({model.table_name()}.user_ids) WHERE json_each.value = ?)",
                    (user_ids,),
                )
            else:
                cursor.execute(f"SELECT * FROM {model.table_name()}")
            return [self._gen_object(model, row) for row in cursor.fetchall()]

    def get(self, model: type, id: int):
        with self.get_db() as conn:
            cursor = conn.cursor()
            cursor.execute(f"SELECT * FROM {model.table_name()} WHERE id=?", (id,))
            return self._gen_object(model, cursor.fetchone())

    def get_by_field(self, model: type, field: str, value: Any):
        with self.get_db() as conn:
            cursor = conn.cursor()
            cursor.execute(
                f"SELECT * FROM {model.table_name()} WHERE {field}=?", (value,)
            )
            return self._gen_object(model, cursor.fetchone())

    def create(self, model_instance):
        with self.get_db() as conn:
            cursor = conn.cursor()
            del model_instance.id
            query, values = self._gen_insert_query(type(model_instance), model_instance)
            cursor.execute(query, values)
            model_instance.id = cursor.lastrowid
            conn.commit()
            return model_instance

    def update(self, model_instance, exclude_password: bool = False):
        with self.get_db() as conn:
            cursor = conn.cursor()
            id = model_instance.id
            query, values = self._gen_insert_query(
                type(model_instance),
                model_instance,
                id,
                exclude_password=exclude_password,
            )
            cursor.execute(query, values)
            conn.commit()
            return model_instance

    def delete(self, model_instance) -> bool:
        with self.get_db() as conn:
            cursor = conn.cursor()
            cursor.execute(
                f"DELETE FROM {model_instance.table_name()} WHERE id=?",
                (model_instance.id,),
            )
            conn.commit()
            return True
