from fastapi import APIRouter, Depends, status
from .. import schemas, database, oauth2, token
from sqlalchemy.orm import Session
from typing import List
from .. repository import blog


router = APIRouter(
    prefix = "/blog",
    tags=['blogs']
)

@router.get('/', response_model=List[schemas.ShowBlog])
def all(db: Session = Depends(database.get_db), get_current_user: schemas.User = Depends(oauth2.get_current_user)):
    return blog.get_all(db)

@router.post('/', status_code=status.HTTP_201_CREATED)
def create(request: schemas.Blog, db: Session = Depends(database.get_db)):
   return blog.create_blog(request, db)

@router.get('/{id}', status_code=200, response_model=schemas.ShowBlog)
def show(id, db: Session = Depends(database.get_db)):
    return blog.show(id, db)

@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def destroy(id, db: Session = Depends(database.get_db)):
    return blog.destroy(id, db)


@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED)
def update(id, request: schemas.Blog, db: Session = Depends(database.get_db)):
    return blog.update(id, request, db)