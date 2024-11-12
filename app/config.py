# app/config.py
import os
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from databases import Database
from dotenv import load_dotenv

# Cargar las variables de entorno
load_dotenv()

# Variables de conexión
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Configuración de SQLAlchemy
engine = create_engine(DATABASE_URL)
Base = declarative_base()

# Configuración de Database (asíncrona)
database = Database(DATABASE_URL)
