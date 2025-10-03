from fastapi import FastAPI
import models
from database import engine
from routers import auth_router, products_router, customers_router, orders_router

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="FastAPI User Auth Example")

app.include_router(auth_router.router)
app.include_router(products_router.router)
app.include_router(customers_router.router)
app.include_router(orders_router.router)


