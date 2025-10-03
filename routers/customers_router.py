from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import models
from database import get_db
import schemas, crud

router = APIRouter(prefix="/api/customers", tags=["Customers"])

@router.get("/", response_model=list[schemas.CustomerRead])
def list_customers(
    skip: int = 0,
    limit: int = 100,
    full_name: str | None = None,
    email: str | None = None,
    db: Session = Depends(get_db)
):
    query = db.query(models.Customer)

    if full_name:
        query = query.filter(models.Customer.full_name.ilike(f"%{full_name}%"))
    if email:
        query = query.filter(models.Customer.email.ilike(f"%{email}%"))

    return query.offset(skip).limit(limit).all()


@router.post("/", response_model=schemas.CustomerRead)
def create_customer(customer: schemas.CustomerCreate, db: Session = Depends(get_db)):
    return crud.create_customer(db, customer)

@router.get("/{customer_id}", response_model=schemas.CustomerRead)
def get_customer(customer_id: int, db: Session = Depends(get_db)):
    customer = crud.get_customer(db, customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer

@router.put("/{customer_id}", response_model=schemas.CustomerRead)
def update_customer(customer_id: int, customer: schemas.CustomerCreate, db: Session = Depends(get_db)):
    updated = crud.update_customer(db, customer_id, customer)
    if not updated:
        raise HTTPException(status_code=404, detail="Customer not found")
    return updated

@router.delete("/{customer_id}", response_model=schemas.CustomerRead)
def delete_customer(customer_id: int, db: Session = Depends(get_db)):
    deleted = crud.delete_customer(db, customer_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Customer not found")
    return deleted
