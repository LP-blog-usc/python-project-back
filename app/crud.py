# app/crud.py
from sqlalchemy.orm import Session
from sqlalchemy import func, extract
from datetime import datetime, timedelta
from app.models import CreditPurchase, Product, User, Product, Reservation, CreditAccount, CreditPurchase
from app.schemas import ProductStatistics, ProductCreate, ProductUpdate, CreditAccountCreate, CreditPurchaseCreate, ReservationCreate 
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

def create_reservation(db: Session, reservation: ReservationCreate):
    db_reservation = Reservation(
        product_id=reservation.product_id,
        quantity=reservation.quantity,
        payment_method=reservation.payment_method
    )
    db.add(db_reservation)
    db.commit()
    db.refresh(db_reservation)
    return db_reservation

def get_all_reservations(db: Session):
    return db.query(Reservation).all()

def create_credit_account(db: Session, account: CreditAccountCreate):
    db_account = CreditAccount(
        customer_name=account.customer_name,
        total_credit=0.0,
        pending_balance=0.0
    )
    db.add(db_account)
    db.commit()
    db.refresh(db_account)
    return db_account

def register_credit_purchase(db: Session, purchase: CreditPurchaseCreate):
    db_account = db.query(CreditAccount).filter(CreditAccount.id == purchase.account_id).first()
    if not db_account:
        raise HTTPException(status_code=404, detail="Credit account not found")

    # Crear la compra a crédito
    db_purchase = CreditPurchase(
        account_id=purchase.account_id,
        product_id=purchase.product_id,
        amount=purchase.amount,
        status="pending"
    )
    db_account.total_credit += purchase.amount
    db_account.pending_balance += purchase.amount

    db.add(db_purchase)
    db.commit()
    db.refresh(db_account)
    return db_purchase

def get_credit_account_balance(db: Session, account_id: int):
    return db.query(CreditAccount).filter(CreditAccount.id == account_id).first()

def get_sales_report(db: Session, start_date: datetime, end_date: datetime):
    # Total de ventas en el rango de fechas
    total_sales = db.query(func.sum(CreditPurchase.amount)).filter(
        CreditPurchase.status == "paid",
        CreditPurchase.date >= start_date,
        CreditPurchase.date < end_date
    ).scalar() or 0.0

    # Productos vendidos en el rango de fechas
    product_sales = db.query(
        Product.id,
        Product.name,
        func.sum(CreditPurchase.amount).label("total_sold")
    ).join(CreditPurchase, CreditPurchase.product_id == Product.id).filter(
        CreditPurchase.status == "paid",
        CreditPurchase.date >= start_date,
        CreditPurchase.date < end_date
    ).group_by(Product.id).all()

    # Convertir a formato ProductStatistics
    products_sold = [
        ProductStatistics(
            product_id=row.id,
            product_name=row.name,
            total_sold=row.total_sold
        )
        for row in product_sales
    ]

    return {
        "total_sales": total_sales,
        "products_sold": products_sold
    }

def get_date_range(period: str):
    today = datetime.today()
    if period == "daily":
        start_date = today.replace(hour=0, minute=0, second=0, microsecond=0)
        end_date = start_date + timedelta(days=1)
    elif period == "weekly":
        start_date = today - timedelta(days=today.weekday())  # Lunes de esta semana
        end_date = start_date + timedelta(days=7)
    elif period == "monthly":
        start_date = today.replace(day=1)
        end_date = (start_date + timedelta(days=32)).replace(day=1)  # Primer día del próximo mes
    else:
        raise ValueError("Periodo inválido")
    return start_date, end_date