import os
from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context
from app import db
from app.models import *  # Importez vos modèles

# Configure Alembic
config = context.config

# Configure les logs
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Lire DATABASE_URL depuis l'environnement
database_url = os.getenv("DATABASE_URL")
if not database_url:
    raise ValueError("La variable d'environnement DATABASE_URL est manquante.")
config.set_main_option("sqlalchemy.url", database_url)

# Configurer les métadonnées cibles (vos modèles SQLAlchemy)
target_metadata = db.metadata

def run_migrations_offline():
    """Exécute les migrations hors ligne."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url, target_metadata=target_metadata, literal_binds=True, dialect_opts={"paramstyle": "named"}
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    """Exécute les migrations en ligne."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
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
