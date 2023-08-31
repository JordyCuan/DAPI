from typing import Optional

from pydantic import BaseModel, ConfigDict


class CreateUser(BaseModel):
    username: str
    email: Optional[str]
    firstname: str
    lastname: str
    password: str

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "username": "Spider Boy",
                    "email": "pedro@spider.com",
                    "firstname": "Pedro",
                    "lastname": "Lander",
                    "password": "my_password",
                },
            ]
        }
    )
