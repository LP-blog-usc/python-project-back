# app/models.py
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from app.config import Base
from sqlalchemy.orm import relationship
from datetime import datetime

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(100), nullable=False) 

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(String(255), nullable=True)
    price = Column(Float, nullable=False)
    quantity = Column(Integer, nullable=False)

    # Relación con las reservas
    reservations = relationship("Reservation", back_populates="product")
    sales = relationship("Sale", back_populates="product")

class Reservation(Base):
    __tablename__ = "reservations"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    payment_method = Column(String(50), nullable=False)  # Indica el método de pago

    # Relación con el producto
    product = relationship("Product", back_populates="reservations")

class CreditAccount(Base):
    __tablename__ = "credit_accounts"

    id = Column(Integer, primary_key=True, index=True)
    customer_name = Column(String(100), nullable=False)
    total_credit = Column(Float, nullable=False, default=0.0)  # Total monto en crédito
    pending_balance = Column(Float, nullable=False, default=0.0)  # Saldo pendiente

    # Relación con las compras a crédito
    purchases = relationship("CreditPurchase", back_populates="account")

class CreditPurchase(Base):
    __tablename__ = "credit_purchases"

    id = Column(Integer, primary_key=True, index=True)
    account_id = Column(Integer, ForeignKey("credit_accounts.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    amount = Column(Float, nullable=False)  # Monto de la compra
    status = Column(String(50), nullable=False, default="pending")  # Estado de la compra ("pending" o "paid")
    date = Column(DateTime, default=datetime.now)  # Fecha de la compra

    # Relaciones con cuentas de crédito y productos
    account = relationship("CreditAccount", back_populates="purchases")
    product = relationship("Product")

class Sale(Base):
    __tablename__ = "sales"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    total_price = Column(Float, nullable=False)
    date = Column(DateTime, nullable=False)

    product = relationship("Product", back_populates="sales")

