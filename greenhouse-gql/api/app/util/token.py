from datetime import timedelta
from typing import Any

from flask import current_app
from itsdangerous import URLSafeTimedSerializer


def get_serializer(namespace: str) -> URLSafeTimedSerializer:
    secret_key = current_app.config["SECRET_KEY"]
    return URLSafeTimedSerializer(secret_key, salt=namespace)


def create_token(data: Any, namespace: str) -> str:
    return get_serializer(namespace).dumps(data)


def get_token_data(token: str, namespace: str, expiration: timedelta) -> Any:
    return get_serializer(namespace).loads(
        token, max_age=expiration.total_seconds() if expiration is not None else None
    )
