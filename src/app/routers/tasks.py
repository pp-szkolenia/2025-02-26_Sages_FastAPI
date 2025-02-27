from fastapi import HTTPException, status, Response, APIRouter, Depends
from fastapi.responses import JSONResponse

from app.utils import get_item_index_by_id, get_item_by_id
from app.models import (
    TaskBody, TaskResponse, GetAllTasksResponse,
    GetSingleTaskResponse, CreateTaskResponse,
    UpdateTaskResponse, Error404, Error404Message)
from db.utils import connect_to_db


router = APIRouter()


tasks_data = [
    {"description": "Learn FastAPI", "id": 1,  "priority": 3, "is_completed": True},
    {"id": 2, "description": "Do exercises", "priority": 2, "is_completed": False},
]


@router.get("/tasks", tags=["tasks"], response_model=GetAllTasksResponse)
def get_tasks(conn_cursor: tuple = Depends(connect_to_db)):
    conn, cursor = conn_cursor

    cursor.execute("SELECT * FROM tasks")
    tasks_data = cursor.fetchall()
    # records = db_connector.get_records(table_name)

    return {"result": tasks_data}


@router.get("/tasks/{task_id}", tags=["tasks"])
def get_task_by_id(task_id: int):
    conn, cursor = connect_to_db()
    cursor.execute("SELECT * FROM tasks WHERE id = %s", (task_id,))
    target_task = cursor.fetchone()
    conn.close()
    cursor.close()

    if not target_task:
        message = {"error1": f"Task {task_id} not found."}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=message)

    return {"result": target_task}
    # return JSONResponse(status_code=status.HTTP_200_OK, content={"result": target_task})



@router.post("/tasks", status_code=status.HTTP_201_CREATED, tags=["tasks"])
def create_task(body: TaskBody):
    conn, cursor = connect_to_db()

    insert_query_template = f"""INSERT INTO tasks (description, priority, is_completed)
                                VALUES (%s, %s, %s) RETURNING *"""
    insert_query_values = [body.description, body.priority, body.is_completed]

    cursor.execute(insert_query_template, insert_query_values)
    new_task = cursor.fetchone()
    conn.commit()

    conn.close()
    cursor.close()

    return JSONResponse(content={"message": "New task added", "details": new_task},
                        status_code=status.HTTP_202_ACCEPTED)


@router.delete("/tasks/{task_id}", tags=["tasks"])
def delete_task_by_id(task_id: int):
    conn, cursor = connect_to_db()

    delete_query = "DELETE FROM tasks WHERE id = %s RETURNING *;"
    cursor.execute(delete_query, (task_id,))
    deleted_task = cursor.fetchone()
    conn.commit()

    conn.close()
    cursor.close()

    if not deleted_task:
        message = {"error": f"Task {task_id} not found."}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=message)

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/tasks/{task_id}", tags=["tasks"])
def update_task_by_id(task_id: int, body: TaskBody):
    conn, cursor = connect_to_db()

    update_query = """
        UPDATE tasks
        SET description = %s, priority = %s, is_completed = %s WHERE id = %s RETURNING *;"""
    cursor.execute(update_query, (body.description, body.priority, body.is_completed, task_id))
    updated_task = cursor.fetchone()
    conn.commit()

    conn.close()
    cursor.close()

    if not updated_task:
        message = {"error": f"Task {task_id} not found."}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=message)

    message = {"message": f"Task {task_id} updated", "new_value": updated_task}
    return JSONResponse(status_code=status.HTTP_200_OK, content=message)
