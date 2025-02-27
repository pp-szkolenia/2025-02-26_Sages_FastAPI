from fastapi import HTTPException, status, Response, APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from db.orm import get_session
from db.models import User
from app.utils import get_item_index_by_id, get_item_by_id
from app.models import UserBody


router = APIRouter(tags=["users"], prefix="/users")

users_data = [
    {"id": 1, "username": "Andrzej", "password": "qwerty123", "is_admin": True},
    {"id": 2, "username": "Andżela", "password": "hasło1!", "is_admin": False}
]


@router.get("")
def get_users(session: Session = Depends(get_session)):
    users_data = session.query(User).all()
    # return JSONResponse(status_code=status.HTTP_200_OK, content={"result": users_data})
    return {"result": users_data}


@router.get("/{user_id}")
def get_user_by_id(user_id: int, session: Session = Depends(get_session)):
    # target_user = get_item_by_id(users_data, user_id)
    target_user = session.query(User).filter_by(id_number=user_id).first()

    if not target_user:
        message = {"error": f"User {user_id} not found."}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=message)

    return {"result": target_user}
    # return JSONResponse(status_code=status.HTTP_200_OK, content={"result": target_user})


@router.post("", status_code=status.HTTP_201_CREATED)
def create_user(body: UserBody, session: Session = Depends(get_session)):
    new_user = body.model_dump()
    new_user = User(**new_user)
    session.add(new_user)
    session.commit()
    session.refresh(new_user)

    return {"message": "New user added", "details": new_user}

    # return JSONResponse(status_code=status.HTTP_201_CREATED,
    #                     content={"message": "New user added", "details": new_user.__dict__})


@router.delete("/{user_id}")
def delete_user_by_id(user_id: int, session: Session = Depends(get_session)):
    deleted_user = session.query(User).filter_by(id_number=user_id).first()

    if not deleted_user:
        message = {"error": f"User {user_id} not found."}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=message)

    session.delete(deleted_user)
    session.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{user_id}")
def update_user_by_id(user_id: int, body: UserBody, session: Session = Depends(get_session)):
    filter_query = session.query(User).filter_by(id_number=user_id)

    if not filter_query.first():
        message = {"error": f"User {user_id} not found."}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=message)

    filter_query.update(body.model_dump())
    session.commit()
    updated_user = filter_query.first()

    return {"message": f"User {user_id} updated", "new_value": updated_user}
    # return JSONResponse(status_code=status.HTTP_200_OK, content=message)
