
from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional
from datetime import datetime
from models import OrderStatus


class UserBase(BaseModel):
    full_name: str
    email: EmailStr

class UserCreate(UserBase):
    password: str
    is_admin: Optional[bool] = False

class UserOut(UserBase):
    id: int
    is_admin: bool

    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str




class ProductBase(BaseModel):
    name: str
    price: float = Field(ge=0)
    qty_in_stock: int = Field(ge=0)

class ProductCreate(ProductBase):
    sku: str

class ProductRead(ProductBase):
    id: int
    slug: str
    is_active: bool
    class Config: from_attributes = True



class CustomerBase(BaseModel):
    full_name: str
    email: EmailStr
    phone: str

class CustomerCreate(CustomerBase):
    pass

class CustomerRead(CustomerBase):
    id: int
    class Config: from_attributes = True



class OrderItemCreate(BaseModel):
    product_id: int
    qty: int

class OrderItemRead(BaseModel):
    id: int
    product_id: int
    qty: int
    unit_price: float
    line_total: float
    class Config: from_attributes = True



class OrderCreate(BaseModel):
    customer_id: int
    items: List[OrderItemCreate]

class OrderRead(BaseModel):
    id: int
    customer_id: int
    status: OrderStatus
    total: float
    created_at: datetime
    items: List[OrderItemRead]
    class Config: from_attributes = True
