from passlib.context import CryptContext


class BCryptContext:
    def __init__(self, schemes=["bcrypt"], deprecated="auto", **kwargs) -> None:
        self.bcrypt_context = CryptContext(schemes=schemes, deprecated=deprecated, **kwargs)

    def get_password_hash(self, password: str):
        return self.bcrypt_context.hash(password)

    def verify_password(self, plain_password, hashed_password):
        return self.bcrypt_context.verify(plain_password, hashed_password)


def get_bcrypt_context(**kwargs):
    return BCryptContext(**kwargs)
