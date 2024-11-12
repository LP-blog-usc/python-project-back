# app/endpoints/products.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas import ProductCreate, ProductUpdate, ProductResponse, SaleRequest
from app.crud import process_sale, create_product, get_product_by_id, update_product, delete_product, get_all_products
from app.config import engine
from typing import List

router = APIRouter()

# Dependency
def get_db():
    db = Session(bind=engine)
    try:
        yield db
    finally:
        db.close()

@router.post("/products", response_model=ProductResponse)
def add_product(product: ProductCreate, db: Session = Depends(get_db)):
    db_product = create_product(db, product)
    return db_product

@router.put("/products/{product_id}", response_model=ProductResponse)
def edit_product(product_id: int, product: ProductUpdate, db: Session = Depends(get_db)):
    db_product = update_product(db, product_id, product)
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product

@router.delete("/products/{product_id}", response_model=ProductResponse)
def remove_product(product_id: int, db: Session = Depends(get_db)):
    db_product = delete_product(db, product_id)
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product

@router.get("/products", response_model=List[ProductResponse])
def list_products(db: Session = Depends(get_db)):
    products = get_all_products(db)
    return products

@router.post("/products/sale", response_model=ProductResponse)
def make_sale(sale: SaleRequest, db: Session = Depends(get_db)):
    db_product = process_sale(db, sale.product_id, sale.quantity)
    return db_product