from fastapi import FastAPI

from app.api import router


app = FastAPI(title="Task Management API")


app.include_router(router)


@app.get("/")
def root():
    return {"message": "Task Management API is running"}