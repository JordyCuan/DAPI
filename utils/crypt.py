from typing import Any

from passlib.context import CryptContext


class BCryptContext:
    def __init__(self, schemes: list[str] = ["bcrypt"], deprecated: str = "auto", **kwargs: Any) -> None:
        self.bcrypt_context = CryptContext(schemes=schemes, deprecated=deprecated, **kwargs)

    def get_password_hash(self, password: str) -> str:
        return self.bcrypt_context.hash(password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return self.bcrypt_context.verify(plain_password, hashed_password)


def get_bcrypt_context(**kwargs: Any) -> BCryptContext:
    return BCryptContext(**kwargs)
