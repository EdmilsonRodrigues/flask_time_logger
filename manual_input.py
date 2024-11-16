import requests
from config import BASE_API_URL
from models.users import User
from session import db


def main():
    url = BASE_API_URL
    path = "/test-api"
    data = {"key": "value", "value": "key"}
    response = requests.post(url + path, json=data)
    print(response.json())


def test_get_schemas():
    print(
        db._gen_insert_query(
            User,
            User(
                id=1,
                name="name",
                email="email",
                password="password",
                department="department",
                role="role",
            ),
            id=1,
        )
    )


if __name__ == "__main__":
    test_get_schemas()
