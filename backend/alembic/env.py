
import os

from dotenv import load_dotenv

from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import create_engine, pool

from alembic import context

load_dotenv()

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

from app.models import Base
from app.models.user import User
from app.models.mansei import ManseiResult

target_metadata = Base.metadata

def run_migrations_offline() -> None:

    url = os.environ.get("DATABASE_URL")
    if not url:
        raise ValueError("DATABASE_URL 환경변수가 설정되지 않았습니다.")

    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    url = os.environ.get("DATABASE_URL")
    if not url:
        raise ValueError("DATABASE_URL 환경변수가 설정되지 않았습니다.")


    connectable = create_engine(url, poolclass=pool.NullPool)
    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
