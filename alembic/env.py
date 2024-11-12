from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context

# Importa la URL de la base de datos y el modelo Base desde config.py
from app.config import DATABASE_URL, Base
import app.models  # Asegura que Alembic detecte los modelos al cargar el módulo

# Configuración de Alembic
config = context.config

# Establece la URL de la base de datos en el archivo de configuración de Alembic
config.set_main_option("sqlalchemy.url", DATABASE_URL)

# Configura el logger
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Define target_metadata para que Alembic detecte las migraciones automáticamente
target_metadata = Base.metadata

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
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
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

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
