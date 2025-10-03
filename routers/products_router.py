# from fastapi import APIRouter, Depends, HTTPException
# from sqlalchemy.orm import Session
# from database import get_db
# import models, schemas
# from slugify import slugify
#
# router = APIRouter(prefix="/api/products", tags=["Products"])
#
#
# @router.get("/", response_model=list[schemas.ProductRead])
# def list_products(db: Session = Depends(get_db)):
#     return db.query(models.Product).all()
#
#
# @router.post("/", response_model=schemas.ProductRead)
# def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
#     slug = slugify(product.name)
#     db_product = models.Product(
#         name=product.name,
#         slug=slug,
#         sku=product.sku,
#         price=product.price,
#         qty_in_stock=product.qty_in_stock,
#     )
#     db.add(db_product)
#     db.commit()
#     db.refresh(db_product)
#     return db_product


from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import schemas, crud

router = APIRouter(prefix="/api/products", tags=["Products"])

@router.get("/", response_model=list[schemas.ProductRead])
def list_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.list_products(db, skip, limit)

@router.post("/", response_model=schemas.ProductRead)
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    return crud.create_product(db, product)

@router.get("/{product_id}", response_model=schemas.ProductRead)
def get_product(product_id: int, db: Session = Depends(get_db)):
    db_product = crud.get_product(db, product_id)
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product

@router.put("/{product_id}", response_model=schemas.ProductRead)
def update_product(product_id: int, product: schemas.ProductCreate, db: Session = Depends(get_db)):
    updated = crud.update_product(db, product_id, product)
    if not updated:
        raise HTTPException(status_code=404, detail="Product not found")
    return updated

@router.delete("/{product_id}", response_model=schemas.ProductRead)
def delete_product(product_id: int, db: Session = Depends(get_db)):
    deleted = crud.delete_product(db, product_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Product not found")
    return deleted
