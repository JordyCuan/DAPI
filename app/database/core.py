from sqlalchemy import Engine, create_engine
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import Session, sessionmaker

from app.settings import settings


def get_engine() -> Engine:
    return create_engine(
        settings.get_database_url(),
        pool_pre_ping=True,
        # pool_size=settings.pool_size,
        # max_overflow=settings.max_overflow
    )


def get_session_maker(engine: Engine) -> sessionmaker[Session]:
    return sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine,
    )


engine = get_engine()
session_maker = get_session_maker(engine)


__all__ = [
    "engine",
    "session_maker",
]


# def get_async_engine(settings):
#     return create_async_engine(
#         settings.get_database_url(),
#         # pool_pre_ping=True,
#         # pool_size=settings.pool_size,
#         # max_overflow=settings.max_overflow
#     )


# def get_async_session_maker(async_engine):
#     return async_sessionmaker(
#         autocommit=False,
#         autoflush=False,
#         bind=async_engine,
#     )


# async_engine = get_async_engine(settings)
# async_session_maker = get_async_session_maker(async_engine)


# def get_async_database():
#     try:
#         db = async_session_maker()
#         yield db
#     finally:
#         db.close()
