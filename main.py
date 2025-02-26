from fastapi import FastAPI, Body


app = FastAPI()

tasks_data = [
    {"description": "Learn FastAPI", "priority": 3, "is_completed": True},
    {"description": "Do exercises", "priority": 2, "is_completed": False},
]

users_data = [
    {"username": "Andrzej", "password": "qwerty123", "is_admin": True},
    {"username": "Andżela", "password": "hasło1!", "is_admin": False}
]


@app.get("/")
def root():
    return {"message": "Hello World!"}


@app.get("/tasks")
def get_tasks():
    return {"result": tasks_data}


@app.get("/users")
def get_users():
    return {"result": users_data}


@app.post("/tasks")
def create_task(body: dict = Body(...)):
    new_task = body
    tasks_data.append(new_task)

    return {"message": "New task added", "details": new_task}
