from utils.database.models import APIBaseModel


# NOTE: Base model for the current app. Used by Alembic
class Base(APIBaseModel):
    __abstract__ = True
