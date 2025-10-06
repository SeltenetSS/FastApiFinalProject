# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware
# import models
# from database import engine
# from routers import auth_router, products_router, customers_router, orders_router, reports_router
#
# models.Base.metadata.create_all(bind=engine)
#
# app = FastAPI(title="MiniERP Backend")
#
# # ✅ CORS ayarları — frontend port 3002 üçün
# origins = [
#     "http://localhost:3002",
#     "http://127.0.0.1:3002",
# ]
#
# # ⚠️ CORS middleware-i *routers* əlavə etməzdən əvvəl yerləşdirməlisən!
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],   # GET, POST, PUT, DELETE, OPTIONS hamısı
#     allow_headers=["*"],   # Content-Type, Authorization, və s.
# )
#
# # ✅ Routers əlavə edilir
# app.include_router(auth_router.router, prefix="/api/auth", tags=["Auth"])
# app.include_router(products_router.router, prefix="/api/products", tags=["Products"])
# app.include_router(customers_router.router, prefix="/api/customers", tags=["Customers"])
# app.include_router(orders_router.router, prefix="/api/orders", tags=["Orders"])
# app.include_router(reports_router.router, prefix="/api/reports", tags=["Reports"])
#
#
# # ✅ Test üçün köməkçi endpoint
# @app.get("/")
# def root():
#     return {"message": "MiniERP API is running ✅"}



from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from fastapi.staticfiles import StaticFiles

import models
from database import engine
from routers import auth_router, products_router, customers_router, orders_router, reports_router

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="MiniERP Backend")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],

    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.mount("/static", StaticFiles(directory="uploads"), name="static")

app.include_router(auth_router.router)
app.include_router(products_router.router)
app.include_router(customers_router.router)
app.include_router(orders_router.router)
app.include_router(reports_router.router)

@app.get("/")
def root():
    return {"message": "MiniERP API is running ✅"}
