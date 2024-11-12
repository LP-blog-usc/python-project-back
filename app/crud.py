# app/crud.py
from sqlalchemy.orm import Session
from app.models import User, Product
from app.schemas import ProductCreate, ProductUpdate
from typing import List

def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

def create_product(db: Session, product: ProductCreate):
    db_product = Product(
        name=product.name,
        description=product.description,
        price=product.price,
        quantity=product.quantity
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def get_product_by_id(db: Session, product_id: int):
    return db.query(Product).filter(Product.id == product_id).first()

def update_product(db: Session, product_id: int, product: ProductUpdate):
    db_product = get_product_by_id(db, product_id)
    if db_product:
        if product.name is not None:
            db_product.name = product.name
        if product.description is not None:
            db_product.description = product.description
        if product.price is not None:
            db_product.price = product.price
        if product.quantity is not None:
            db_product.quantity = product.quantity
        db.commit()
        db.refresh(db_product)
    return db_product

def delete_product(db: Session, product_id: int):
    db_product = get_product_by_id(db, product_id)
    if db_product:
        db.delete(db_product)
        db.commit()
    return db_product

def get_all_products(db: Session) -> List[Product]:
    return db.query(Product).all()

def process_sale(db: Session, product_id: int, quantity: int):
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # Verificar si hay suficiente cantidad en el inventario
    if db_product.quantity < quantity:
        raise HTTPException(status_code=400, detail="Not enough stock for the product")

    # Reducir la cantidad en existencia
    db_product.quantity -= quantity
    db.commit()
    db.refresh(db_product)
    return db_product