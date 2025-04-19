from fastapi import FastAPI

from routers import (
    restaurant_router,
    auth_router,
    customer_router,
    restaurant_manager_router,
    admin_router,
    profile_router,
)

app = FastAPI()


app.include_router(auth_router)
app.include_router(profile_router)
app.include_router(restaurant_router)
app.include_router(admin_router)
app.include_router(customer_router)
app.include_router(restaurant_manager_router)


@app.get("/")
def read_root():
    return {"message": "Welcome to the restaurant reservation system!"}
