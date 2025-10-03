from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import models, schemas
from slugify import slugify

router = APIRouter(prefix="/api/products", tags=["Products"])


@router.get("/", response_model=list[schemas.ProductRead])
def list_products(db: Session = Depends(get_db)):
    return db.query(models.Product).all()


@router.post("/", response_model=schemas.ProductRead)
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    slug = slugify(product.name)
    db_product = models.Product(
        name=product.name,
        slug=slug,
        sku=product.sku,
        price=product.price,
        qty_in_stock=product.qty_in_stock,
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product
