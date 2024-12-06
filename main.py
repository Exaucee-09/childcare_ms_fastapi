from fastapi import FastAPI
from routes.routes import router as api_router
from database import engine
import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(api_router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Childcare Management System"}
