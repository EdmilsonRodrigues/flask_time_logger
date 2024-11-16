from datetime import UTC, datetime, timedelta

import jwt

from config import SECRET_KEY


class Auth:
    @staticmethod
    def gen_jwt(user):
        payload = {
            "user_id": user.id,
            "exp": datetime.now(UTC) + timedelta(days=7),
            "secret": SECRET_KEY,
        }
        return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

    @staticmethod
    def decode_jwt(token: str):
        try:
            return jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None
