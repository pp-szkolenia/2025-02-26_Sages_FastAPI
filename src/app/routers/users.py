from fastapi import HTTPException, status, Response, APIRouter
from fastapi.responses import JSONResponse

from app.utils import get_item_index_by_id, get_item_by_id
from app.models import UserBody


router = APIRouter(tags=["users"], prefix="/users")

users_data = [
    {"id": 1, "username": "Andrzej", "password": "qwerty123", "is_admin": True},
    {"id": 2, "username": "Andżela", "password": "hasło1!", "is_admin": False}
]


@router.get("")
def get_users():
    return JSONResponse(status_code=status.HTTP_200_OK, content={"result": users_data})


@router.get("/{user_id}")
def get_user_by_id(user_id: int):
    target_user = get_item_by_id(users_data, user_id)

    if target_user is None:
        message = {"error": f"User {user_id} not found."}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=message)

    return JSONResponse(status_code=status.HTTP_200_OK, content={"result": target_user})


@router.post("", status_code=status.HTTP_201_CREATED)
def create_user(body: UserBody):
    new_user = body.model_dump()
    new_user_id = max([user["id"] for user in users_data]) + 1
    new_user["id"] = new_user_id
    users_data.append(new_user)

    return JSONResponse(status_code=status.HTTP_201_CREATED,
                        content={"message": "New user added", "details": new_user})


@router.delete("/{user_id}")
def delete_user_by_id(user_id: int):
    target_index = get_item_index_by_id(users_data, user_id)

    if target_index is None:
        message = {"error": f"User {user_id} not found."}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=message)

    users_data.pop(target_index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{user_id}")
def update_user_by_id(user_id: int, body: UserBody):
    target_index = get_item_index_by_id(users_data, user_id)

    if target_index is None:
        message = {"error": f"User {user_id} not found."}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=message)

    updated_user = body.model_dump()
    updated_user["id"] = user_id
    users_data[target_index] = updated_user

    message = {"message": f"User {user_id} updated", "new_value": updated_user}
    return JSONResponse(status_code=status.HTTP_200_OK, content=message)
