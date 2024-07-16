from fastapi import APIRouter, status
from fastapi.security import OAuth2PasswordRequestForm
from .. import schemas, database, models, token
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..hashing import Hash
from typing import Annotated


router = APIRouter(
    tags=['authentication']
)

@router.post('/login')
def login(request:Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email == request.username).first()
    if not user:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"Invalid credentials")
    if not Hash.verify(user.password, request.password):
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"Incorrect Password")

    # access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = token.create_access_token(
        data={"sub": user.email},
        # expires_delta=access_token_expires,
    )
    return {"access_token": access_token, "token_type": "bearer"}
