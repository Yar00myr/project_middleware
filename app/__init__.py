import logging
from fastapi import FastAPI, APIRouter, Request, HTTPException
from pydantic import BaseModel
import uvicorn
from .middleware import HeaderMiddleware, BodyMiddleware

app = FastAPI()

logger = logging.getLogger("middleware_logger")
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)


class Student(BaseModel):
    name: str
    age: int
    grade: str


def setup_middleware():
    app.add_middleware(HeaderMiddleware)
    app.add_middleware(BodyMiddleware)


hello_router = APIRouter(
    prefix="/hello",
)

requests = dict()


@app.get("/")
async def read_root():
    logger.info("Root endpoint accessed")
    return {"message": "Hello World"}


@hello_router.get("/dashboard")
async def dashboard():
    logger.info("Dashboard endpoint accessed")
    return requests


@app.post("/student")
async def students(student: Student):
    logger.info(f"Adding student: {student.name}, {student.age}, {student.grade}")

    requests[student.name] = student.dict()

    logger.info(f"Student {student.name} added successfully")
    return {"message": f"Student {student.name} added successfully!"}


app.include_router(hello_router)

setup_middleware()
