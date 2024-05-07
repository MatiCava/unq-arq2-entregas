from fastapi import FastAPI
from routes.users import users_router
from routes.products import products_router
from routes.seller import sellers_router
from routes.sales import sales_router
from routes.notifications import notifications_router

app = FastAPI()
app.include_router(users_router)
app.include_router(products_router)
app.include_router(sellers_router)
app.include_router(sales_router)
app.include_router(notifications_router)