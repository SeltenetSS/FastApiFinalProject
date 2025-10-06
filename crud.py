

from sqlalchemy.orm import Session
from models import User
from schemas import UserCreate
from auth import hash_password
from sqlalchemy.orm import Session
from models import Product, Customer, Order, OrderItem
from schemas import ProductCreate, CustomerCreate, OrderCreate, OrderItemCreate
from slugify import slugify
from datetime import datetime

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def create_user(db: Session, user: UserCreate):
    db_user = User(
        full_name=user.full_name,
        email=user.email,
        hashed_password=hash_password(user.password),
        is_admin=user.is_admin
    )
    db.add(db_user)
    try:
        db.commit()
        db.refresh(db_user)
        return db_user
    except Exception as e:
        db.rollback()
        raise e






def get_product(db: Session, product_id: int):
    return db.query(Product).filter(Product.id == product_id).first()

def list_products(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Product).offset(skip).limit(limit).all()

def create_product(db: Session, product: ProductCreate):
    db_product = Product(
        name=product.name,
        slug=slugify(product.name),
        sku=product.sku or f"SKU-{slugify(product.name)}",
        price=product.price,
        qty_in_stock=product.qty_in_stock,
        image_url=product.image_url,
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


def update_product(db: Session, product_id: int, updated_data: ProductCreate):
    product = get_product(db, product_id)
    if not product:
        return None
    product.name = updated_data.name
    product.slug = slugify(updated_data.name)
    product.sku = updated_data.sku or f"SKU-{slugify(updated_data.name)}"
    product.price = updated_data.price
    product.qty_in_stock = updated_data.qty_in_stock
    product.image_url = updated_data.image_url
    db.commit()
    db.refresh(product)
    return product


def delete_product(db: Session, product_id: int):
    product = get_product(db, product_id)
    if not product:
        return None
    db.delete(product)
    db.commit()
    return product


def create_customer(db: Session, customer: CustomerCreate):
    db_customer = Customer(
        full_name=customer.full_name,
        email=customer.email,
        phone=customer.phone
    )
    db.add(db_customer)
    try:
        db.commit()
        db.refresh(db_customer)
        return db_customer
    except Exception:
        db.rollback()
        raise

def get_customer(db: Session, customer_id: int):
    return db.query(Customer).filter(Customer.id == customer_id).first()

def list_customers(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Customer).offset(skip).limit(limit).all()

def update_customer(db: Session, customer_id: int, updated_data: CustomerCreate):
    customer = get_customer(db, customer_id)
    if not customer:
        return None
    customer.full_name = updated_data.full_name
    customer.email = updated_data.email
    customer.phone = updated_data.phone
    db.commit()
    db.refresh(customer)
    return customer

def delete_customer(db: Session, customer_id: int):
    customer = get_customer(db, customer_id)
    if not customer:
        return None
    db.delete(customer)
    db.commit()
    return customer


def create_order(db: Session, order_data: OrderCreate):
    order_total = 0
    db_order = Order(
        customer_id=order_data.customer_id,
        status="NEW",
        created_at=datetime.utcnow()
    )
    db.add(db_order)
    db.commit()
    db.refresh(db_order)

    for item in order_data.items:
        product = db.query(Product).filter(Product.id == item.product_id).first()
        if not product or product.qty_in_stock < item.qty:
            raise Exception(f"Not enough stock for product {item.product_id}")
        line_total = item.qty * product.price
        db_order_item = OrderItem(
            order_id=db_order.id,
            product_id=product.id,
            qty=item.qty,
            unit_price=product.price,
            line_total=line_total
        )
        product.qty_in_stock -= item.qty
        db.add(db_order_item)
        order_total += line_total

    db_order.total = order_total
    try:
        db.commit()
        db.refresh(db_order)
        return db_order
    except Exception:
        db.rollback()
        raise

def get_order(db: Session, order_id: int):
    return db.query(Order).filter(Order.id == order_id).first()

def list_orders(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Order).offset(skip).limit(limit).all()

def update_order_status(db: Session, order_id: int, status: str):
    order = get_order(db, order_id)
    if not order:
        return None
    order.status = status
    db.commit()
    db.refresh(order)
    return order

def delete_order(db: Session, order_id: int):
    order = get_order(db, order_id)
    if not order:
        return None
    db.delete(order)
    db.commit()
    return order
