from pydantic import BaseModel


class DatabaseProperties(BaseModel):
    engine: str
    name: str
    user: str
    password: str
    host: str
    port: int


class DatabaseSettingsMixin(BaseModel):
    DATABASE: DatabaseProperties

    def get_database_url(self) -> str:
        props = self.DATABASE.dict()
        return "{engine}://{user}:{password}@{host}:{port}/{name}".format(**props)
