from typing import Annotated

from fastapi import Depends

from .database.core import async_sessionmaker, get_async_session

AsyncSession = Annotated[async_sessionmaker, Depends(get_async_session)]
