import requests
from config import BASE_API_URL


def main():
    url = BASE_API_URL
    path = "/test-api"
    data = {"key": "value", "value": "key"}
    response = requests.post(url + path, json=data)
    print(response.json())


if __name__ == "__main__":
    main()
