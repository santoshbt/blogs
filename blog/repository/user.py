from .. import schemas, models
from sqlalchemy.orm import Session
from .. hashing import Hash
from fastapi import Depends, status, HTTPException
from .. import schemas


def create(request: schemas.User, db:Session):
    new_user = models.User(**request.model_dump())
    new_user.password = Hash.bcrypt(new_user.password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def show(id:int, db: Session):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"User with id {id} not found")
    return user