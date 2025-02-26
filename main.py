from fastapi import FastAPI, HTTPException, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel


app = FastAPI()


class TaskBody(BaseModel):
    description: str
    priority: int | None = None
    is_completed: bool = False


class UserBody(BaseModel):
    username: str
    password: str
    is_admin: bool = False


tasks_data = [
    {"id": 1, "description": "Learn FastAPI", "priority": 3, "is_completed": True},
    {"id": 2, "description": "Do exercises", "priority": 2, "is_completed": False},
]

users_data = [
    {"id": 1, "username": "Andrzej", "password": "qwerty123", "is_admin": True},
    {"id": 2, "username": "Andżela", "password": "hasło1!", "is_admin": False}
]


def get_item_by_id(items_list, item_id):
    for item in items_list:
        if item["id"] == item_id:
            return item
    return None


@app.get("/")
def root():
    return {"message": "Hello World!"}


@app.get("/tasks")
def get_tasks():
    return JSONResponse(status_code=status.HTTP_200_OK, content={"result": tasks_data})


@app.get("/users")
def get_users():
    return {"result": users_data}


@app.get("/users/{user_id}")
def get_user_by_id(user_id: int):
    target_user = get_item_by_id(users_data, user_id)

    if target_user is None:
        message = {"error": f"User {user_id} not found."}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=message)

    return {"result": target_user}


@app.get("/tasks/{task_id}")
def get_task_by_id(task_id: int):
    target_task = get_item_by_id(tasks_data, task_id)
    if target_task is None:
        message = {"error": f"Task {task_id} not found."}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=message)

    return {"result": target_task}


@app.post("/tasks", status_code=status.HTTP_201_CREATED)
def create_task(body: TaskBody):
    new_task = body.model_dump()
    new_task_id = max([task["id"] for task in tasks_data]) + 1
    new_task["id"] = new_task_id

    tasks_data.append(new_task)

    return JSONResponse(content={"message": "New task added", "details": new_task},
                        status_code=status.HTTP_202_ACCEPTED)


@app.post("/users")
def create_user(body: UserBody):
    new_user = body.model_dump()
    new_user_id = max([user["id"] for user in users_data]) + 1
    new_user["id"] = new_user_id
    users_data.append(new_user)

    return {"message": "New user added", "details": new_user}

