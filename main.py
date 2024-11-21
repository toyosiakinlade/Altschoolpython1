from fastapi import FastAPI, Form
from typing  import Annotated
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import time


app = FastAPI()


@app.middleware("http")
async def process_time(request, call_next):
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = time.perf_counter()- start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://127.0.0.1:8000"],
    allow_credentials = True,
    allow_methods=["'"],
    allow_headers=["'"],

)


class UsersModel(BaseModel):
        first_name:str
        last_name:str
        age:int
        email:str
        height:float


class Users(UsersModel):
    id: str


my_users = []



@app.get("/")
async def home():
    return {"Welcome to my page"}

@app.post("/users")
async def create_users(
    first_name: Annotated[str,Form()],
    last_name : Annotated[str,Form()],
    age: Annotated[int,Form()],
    email: Annotated[str,Form()],
    height: Annotated[float,Form()],
):
    
    id = len(my_users) + 1
    new_user = Users(
        first_name=first_name,
        last_name = last_name,
        age = age,
        email = email,
        height = height,
        id = id,
    )

    my_users.append(new_user)
    return {"Successfully created"}
