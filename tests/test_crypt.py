from passlib.context import CryptContext

from utils.crypt import BCryptContext, get_bcrypt_context


def test_bcrypt_context_initialization():
    context = BCryptContext()
    assert isinstance(context.bcrypt_context, CryptContext)
    assert "bcrypt" in context.bcrypt_context.schemes()


def test_get_password_hash():
    context = BCryptContext()
    password = "test_password"
    hashed_password = context.get_password_hash(password)
    assert password != hashed_password
    assert hashed_password.startswith("$2b$")


def test_verify_password():
    context = BCryptContext()
    password = "test_password"
    hashed_password = context.get_password_hash(password)

    assert context.verify_password(password, hashed_password)
    assert not context.verify_password("wrong_password", hashed_password)


def test_get_bcrypt_context():
    context = get_bcrypt_context()
    assert isinstance(context, BCryptContext)
