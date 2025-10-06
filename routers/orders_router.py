# from fastapi import APIRouter, Depends, HTTPException
# from sqlalchemy.orm import Session
#
# import models
# from database import get_db
# import schemas, crud
#
# router = APIRouter(prefix="/api/orders", tags=["Orders"])
#
# @router.get("/", response_model=list[schemas.OrderRead])
# def list_orders(
#     skip: int = 0,
#     limit: int = 100,
#     status: str | None = None,
#     customer_id: int | None = None,
#     db: Session = Depends(get_db)
# ):
#     query = db.query(models.Order)
#
#     if status:
#         query = query.filter(models.Order.status == status)
#     if customer_id:
#         query = query.filter(models.Order.customer_id == customer_id)
#
#     return query.offset(skip).limit(limit).all()
#
# @router.post("/", response_model=schemas.OrderRead)
# def create_order(order: schemas.OrderCreate, db: Session = Depends(get_db)):
#     try:
#         return crud.create_order(db, order)
#     except Exception as e:
#         raise HTTPException(status_code=400, detail=str(e))
#
# @router.get("/{order_id}", response_model=schemas.OrderRead)
# def get_order(order_id: int, db: Session = Depends(get_db)):
#     db_order = crud.get_order(db, order_id)
#     if not db_order:
#         raise HTTPException(status_code=404, detail="Order not found")
#     return db_order
#
# @router.put("/{order_id}/status")
# def update_order_status(order_id: int, status: str, db: Session = Depends(get_db)):
#     updated = crud.update_order_status(db, order_id, status)
#     if not updated:
#         raise HTTPException(status_code=404, detail="Order not found")
#     return updated
#
# @router.delete("/{order_id}", response_model=schemas.OrderRead)
# def delete_order(order_id: int, db: Session = Depends(get_db)):
#     deleted = crud.delete_order(db, order_id)
#     if not deleted:
#         raise HTTPException(status_code=404, detail="Order not found")
#     return deleted


from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel

import models
from database import get_db
import schemas, crud

router = APIRouter(prefix="/api/orders", tags=["Orders"])

@router.get("/", response_model=list[schemas.OrderRead])
def list_orders(
    skip: int = 0,
    limit: int = 100,
    status: str | None = None,
    customer_id: int | None = None,
    db: Session = Depends(get_db)
):
    query = db.query(models.Order)

    if status:
        query = query.filter(models.Order.status == status)
    if customer_id:
        query = query.filter(models.Order.customer_id == customer_id)

    return query.offset(skip).limit(limit).all()

@router.post("/", response_model=schemas.OrderRead)
def create_order(order: schemas.OrderCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_order(db, order)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{order_id}", response_model=schemas.OrderRead)
def get_order(order_id: int, db: Session = Depends(get_db)):
    db_order = crud.get_order(db, order_id)
    if not db_order:
        raise HTTPException(status_code=404, detail="Order not found")
    return db_order

# ✅ YENİ: Status Body ilə qəbul edilsin
class StatusUpdate(BaseModel):
    status: str

@router.put("/{order_id}/status")
def update_order_status(order_id: int, data: StatusUpdate, db: Session = Depends(get_db)):
    updated = crud.update_order_status(db, order_id, data.status)
    if not updated:
        raise HTTPException(status_code=404, detail="Order not found")
    return updated

@router.delete("/{order_id}", response_model=schemas.OrderRead)
def delete_order(order_id: int, db: Session = Depends(get_db)):
    deleted = crud.delete_order(db, order_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Order not found")
    return deleted
