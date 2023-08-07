from typing import Optional

from pydantic import BaseModel, Field


class Todo(BaseModel):
    title: str
    description: Optional[str]
    priority: int = Field(ge=1, le=5, description="Must be between 1-5")
    complete: bool

    class Config:
        schema_extra = {
            "example": {
                "complete": False,
                "description": "A very nice Item",
                "priority": 4,
                "title": "Foo",
            }
        }
