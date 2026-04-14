from logging.config import fileConfig

from alembic import context
from sqlmodel import SQLModel

from src.configs import SETTINGS

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Override URL from settings (convert async to sync for Alembic)
url = SETTINGS.database.url.replace("+asyncpg", "+psycopg")
config.set_main_option("sqlalchemy.url", url)

# Import all models so Alembic can detect them
import src.db.models.users  # noqa: F401
import src.db.models.conversations  # noqa: F401
import src.db.models.nhanh  # noqa: F401
import src.db.models.files  # noqa: F401

target_metadata = SQLModel.metadata


def run_migrations_offline() -> None:
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    from sqlalchemy import create_engine

    connectable = create_engine(url)

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
