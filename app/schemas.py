# app/schemas.py
from pydantic import BaseModel, Field
from enum import Enum
from typing import List, Optional
from datetime import date

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

class PaymentMethod(str, Enum):
    contra_entrega = "contra_entrega"
    tarjeta = "tarjeta"
    efectivo = "efectivo"

class ReservationCreate(BaseModel):
    product_id: int
    quantity: int
    payment_method: PaymentMethod = Field(..., description="Método de pago: contra_entrega o anticipado")

class ReservationResponse(BaseModel):
    id: int
    product_id: int
    quantity: int
    payment_method: str

    class Config:
        orm_mode = True

class CreditAccountCreate(BaseModel):
    customer_name: str

class CreditPurchaseCreate(BaseModel):
    account_id: int
    product_id: int
    amount: float

class CreditAccountResponse(BaseModel):
    id: int
    customer_name: str
    total_credit: float
    pending_balance: float

    class Config:
        orm_mode = True

class ProductStatistics(BaseModel):
    product_id: int
    product_name: str
    total_sold: int 

class ProductSales(BaseModel):
    product_id: int
    product_name: str
    quantity_sold: int

class SalesReport(BaseModel):
    report_date: date
    total_sales: float
    products_sold: List[ProductSales]
    most_sold_products: Optional[List[ProductSales]] = []
    least_sold_products: Optional[List[ProductSales]] = []

    class Config:
        orm_mode = True