from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.core.settings import settings

# Create an asynchronous SQLAlchemy engine using the ASYNC_DATABASE_URI from application settings.
engine = create_async_engine(
    settings.ASYNC_DATABASE_URI, 
)

# Create an AsyncSession class using sessionmaker, bound to the SQLAlchemy engine.
# This session class will be used to interact with the database asynchronously.
SessionLocal = sessionmaker(
    engine, expire_on_commit=False, class_=AsyncSession
)