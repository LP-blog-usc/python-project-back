# app/schemas.py
from pydantic import BaseModel

class UserLogin(BaseModel):
    username: str
    password: str

class ProductBase(BaseModel):
    name: str
    description: str = None
    price: float
    quantity: int

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    name: str = None
    description: str = None
    price: float = None
    quantity: int = None

class ProductResponse(ProductBase):
    id: int

    class Config:
        orm_mode = True

class SaleRequest(BaseModel):
    product_id: int
    quantity: int