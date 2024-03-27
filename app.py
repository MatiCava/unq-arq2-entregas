from fastapi import FastAPI
from routes.users import users_router
from routes.products import products_router
from routes.seller import sellers_router

app = FastAPI()
app.include_router(users_router)
app.include_router(products_router)
app.include_router(sellers_router)