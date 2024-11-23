# app/endpoints/products.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas import SalesReport, CreditAccountCreate, CreditPurchaseCreate, CreditAccountResponse, ReservationCreate, ReservationResponse, ProductCreate, ProductUpdate, ProductResponse, SaleRequest
from app.crud import get_least_sold_products, get_most_sold_products, get_all_credit_accounts, get_sales_report, get_date_range, create_credit_account, register_credit_purchase, get_credit_account_balance, create_reservation, get_all_reservations, process_sale, create_product, get_product_by_id, update_product, delete_product, get_all_products
from app.config import engine
from typing import List
from datetime import datetime

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

@router.post("/products/reserve", response_model=ReservationResponse)
def make_reservation(reservation: ReservationCreate, db: Session = Depends(get_db)):
    db_reservation = create_reservation(db, reservation)
    return db_reservation

@router.get("/products/reservations", response_model=List[ReservationResponse])
def list_reservations(db: Session = Depends(get_db)):
    reservations = get_all_reservations(db)
    return reservations

@router.post("/credit/accounts", response_model=CreditAccountResponse)
def add_credit_account(account: CreditAccountCreate, db: Session = Depends(get_db)):
    db_account = create_credit_account(db, account)
    return db_account

@router.post("/credit/purchases", response_model=CreditAccountResponse)
def add_credit_purchase(purchase: CreditPurchaseCreate, db: Session = Depends(get_db)):
    db_purchase = register_credit_purchase(db, purchase)
    return db_purchase.account

@router.get("/credit/accounts/{account_id}", response_model=CreditAccountResponse)
def view_credit_account(account_id: int, db: Session = Depends(get_db)):
    db_account = get_credit_account_balance(db, account_id)
    if not db_account:
        raise HTTPException(status_code=404, detail="Credit account not found")
    return db_account

@router.get("/reports/sales/{period}", response_model=SalesReport)
def sales_report(period: str, db: Session = Depends(get_db)):
    try:
        start_date, end_date = get_date_range(period)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    report_data = get_sales_report(db, start_date, end_date)
    most_sold_products = get_most_sold_products(db, start_date, end_date)
    least_sold_products = get_least_sold_products(db, start_date, end_date)

    report = SalesReport(
        report_date=datetime.today().date(),
        total_sales=report_data["total_sales"],
        products_sold=report_data["products_sold"],
        most_sold_products=most_sold_products,
        least_sold_products=least_sold_products,
    )
    return report


@router.get("/credit/accounts", response_model=List[CreditAccountResponse])
def list_credit_accounts(db: Session = Depends(get_db)):
    db_accounts = get_all_credit_accounts(db)
    return db_accounts