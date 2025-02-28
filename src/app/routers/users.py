from fastapi import HTTPException, status, Response, APIRouter, Depends, Query
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy import func, asc, desc

from db.orm import get_session
from db.models import User
from app.models import UserBody, TokenData
from app.utils import hash_password_in_body
from app import oauth2


router = APIRouter(tags=["users"], prefix="/users")

users_data = [
    {"id": 1, "username": "Andrzej", "password": "qwerty123", "is_admin": True},
    {"id": 2, "username": "Andżela", "password": "hasło1!", "is_admin": False}
]


@router.get("")
def get_users(session: Session = Depends(get_session),
              _: TokenData = Depends(oauth2.get_current_user),
              is_admin: bool | None = Query(alias="isAdmin", default=None),
              password_limit: int | None = None,
              sort_username: str | None = None):
    # users_data = User.find_all()
    users_data = session.query(User)
    if is_admin is not None:
        users_data = users_data.filter_by(is_admin=is_admin)

    if password_limit is not None:
        users_data = users_data.filter(func.length(User.password) <= password_limit)

    if sort_username in ["asc", "ascending", "ASC"]:
        users_data = users_data.order_by(asc(User.username))
    elif sort_username in ["desc", "descending", "DESC"]:
        users_data = users_data.order_by(desc(User.username))
    elif sort_username is None:
        pass
    else:
        raise Exception(f"Unknown sort method: {sort_username}")


    result = users_data.all()
    # return JSONResponse(status_code=status.HTTP_200_OK, content={"result": users_data})
    return {"result": result}


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
    body = hash_password_in_body(body)
    new_user = body.model_dump()
    new_user = User(**new_user)
    session.add(new_user)
    session.commit()
    session.refresh(new_user)

    return {"message": "New user added", "details": new_user}

    # return JSONResponse(status_code=status.HTTP_201_CREATED,
    #                     content={"message": "New user added", "details": new_user.__dict__})


@router.delete("/{user_id}")
def delete_user_by_id(user_id: int, session: Session = Depends(get_session),
                      user_data: TokenData = Depends(oauth2.get_current_user)):
    if not user_data.is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                             detail="Only admin can delete users")
    deleted_user = session.query(User).filter_by(id_number=user_id).first()

    if not deleted_user:
        message = {"error": f"User {user_id} not found."}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=message)

    session.delete(deleted_user)
    session.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{user_id}")
def update_user_by_id(user_id: int, body: UserBody, session: Session = Depends(get_session)):
    body = hash_password_in_body(body)
    filter_query = session.query(User).filter_by(id_number=user_id)

    if not filter_query.first():
        message = {"error": f"User {user_id} not found."}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=message)

    filter_query.update(body.model_dump())
    session.commit()
    updated_user = filter_query.first()

    return {"message": f"User {user_id} updated", "new_value": updated_user}
    # return JSONResponse(status_code=status.HTTP_200_OK, content=message)
