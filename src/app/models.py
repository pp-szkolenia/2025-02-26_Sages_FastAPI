from pydantic import BaseModel


class TaskBody(BaseModel):
    description: str
    priority: int | None = None
    is_completed: bool = False


class UserBody(BaseModel):
    username: str
    password: str
    is_admin: bool = False


class TaskResponse(BaseModel):
    id: int
    description: str
    priority: int | None
    is_completed: bool


class GetAllTasksResponse(BaseModel):
    result: list[TaskResponse]


class GetSingleTaskResponse(BaseModel):
    result: TaskResponse


class CreateTaskResponse(BaseModel):
    message: str
    details: TaskResponse

class UpdateTaskResponse(BaseModel):
    message: str
    new_value: TaskResponse

class Error404Message(BaseModel):
    error: str

class Error404(BaseModel):
    error: Error404Message


class UserLogin(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    user_id: int
