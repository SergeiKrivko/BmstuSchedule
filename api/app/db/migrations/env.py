# ruff: noqa: F401

from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config, pool

from app.db.database import metadata
from app.models.audience import Audience
from app.models.base import Base
from app.models.course import Course
from app.models.department import Department
from app.models.discipline import Discipline
from app.models.faculty import Faculty
from app.models.filial import Filial
from app.models.group import Group
from app.models.schedule_pair import SchedulePair
from app.models.synchronization import Synchronization
from app.models.teacher import Teacher
from app.models.university import University
from app.settings import db_settings

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

section = config.config_ini_section
settings = db_settings()
config.set_section_option(section, "DB_HOST", settings.host)
config.set_section_option(section, "DB_PORT", str(settings.port))
config.set_section_option(section, "DB_NAME", settings.name)
config.set_section_option(section, "DB_USER", settings.user)
config.set_section_option(section, "DB_PASS", settings.password)

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = [metadata, Base.metadata]

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
