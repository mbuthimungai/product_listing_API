import asyncio
import sys
import pathlib
from alembic import context
from sqlalchemy.ext.asyncio import create_async_engine
# 
from app.models.product import Product
from app.core.settings import settings
from app.models.base import Base_
from sqlalchemy.orm import declarative_base



target_metadata = Base_.metadata
sys.path.append(str(pathlib.Path(__file__).resolve().parents[1]))
def do_run_migrations(connection):
    context.configure(
        compare_type=True,
        dialect_opts={"paramstyle": "named"},
        connection=connection,
        target_metadata=target_metadata,
        include_schemas=True,
        # literal_binds=True,
        version_table_schema=target_metadata.schema,
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online():
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = create_async_engine(settings.ASYNC_DATABASE_URI, future=True)

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)


asyncio.run(run_migrations_online())