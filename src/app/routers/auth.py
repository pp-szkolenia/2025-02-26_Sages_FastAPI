from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session

from db.models import User
from db.orm import get_session
from app.models import UserLogin, Token
from app import utils, oauth2


router = APIRouter(tags=["auth"])


@router.post("/login", response_model=Token)
def login(user_credentials: UserLogin, session: Session = Depends(get_session)):
    user = session.query(User).filter_by(username=user_credentials.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Incorrect username or password")

    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Incorrect username or password")

    payload = {"user_id": user.id_number}
    access_token = oauth2.create_access_token(data=payload)
    return {"access_token": access_token, "token_type": "bearer"}
