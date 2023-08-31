from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class TodoSchema(BaseModel):
    title: str
    description: Optional[str]
    priority: int = Field(ge=1, le=5, description="Must be between 1-5")
    complete: bool

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "complete": False,
                    "description": "A very nice Item",
                    "priority": 4,
                    "title": "Nice Item",
                },
                {
                    "complete": True,
                    "description": "Make my bed at the morning",
                    "priority": 1,
                    "title": "Wake up",
                },
            ]
        }
    )
