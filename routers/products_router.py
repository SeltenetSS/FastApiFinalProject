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

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
import shutil, os
import crud, models, schemas
from database import get_db

router = APIRouter(prefix="/api/products", tags=["Products"])


UPLOAD_DIR = "uploads/products"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/upload-image")
def upload_product_image(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return {"image_url": f"/static/products/{file.filename}"}


@router.post("/", response_model=schemas.ProductRead)
def create_product(
    name: str = Form(...),
    price: float = Form(...),
    qty_in_stock: int = Form(...),
    image: UploadFile | None = File(None),
    db: Session = Depends(get_db)
):
    image_url = None
    if image:
        file_path = os.path.join(UPLOAD_DIR, image.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)
        image_url = f"/static/products/{image.filename}"

    product_data = schemas.ProductCreate(
        name=name,
        price=price,
        qty_in_stock=qty_in_stock,
        image_url=image_url
    )
    return crud.create_product(db, product_data)


@router.get("/", response_model=list[schemas.ProductRead])
def list_products(
    skip: int = 0,
    limit: int = 100,
    name: str | None = None,
    min_price: float | None = None,
    max_price: float | None = None,
    db: Session = Depends(get_db)
):
    query = db.query(models.Product)

    if name:
        query = query.filter(models.Product.name.ilike(f"%{name}%"))
    if min_price is not None:
        query = query.filter(models.Product.price >= min_price)
    if max_price is not None:
        query = query.filter(models.Product.price <= max_price)

    return query.offset(skip).limit(limit).all()


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
