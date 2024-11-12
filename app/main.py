# app/main.py
from fastapi import FastAPI
from app.config import database
from app.endpoints import auth, products  # Importa el router de productos
from app.config import engine

app = FastAPI()

# Conexión a la base de datos
@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

# Incluye el router para autenticación
app.include_router(auth.router, prefix="/auth")
app.include_router(products.router, prefix="/api")
