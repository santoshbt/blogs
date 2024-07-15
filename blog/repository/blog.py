from sqlalchemy.orm import Session
from .. import models
from fastapi import Depends, HTTPException, status
from .. import schemas, database, models

def get_all(db: Session):
    blogs = db.query(models.Blog).all()
    return blogs

def create_blog(request: schemas.Blog, db: Session = Depends(database.get_db)):
    new_blog = models.Blog(title=request.title, body=request.body, user_id=1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

def destroy(id: int, db: Session):
    blog = db.query(models.Blog) \
            .filter(models.Blog.id == id) \

    if not blog.first():
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} not found")

    blog.delete(synchronize_session=False)
    db.commit()
    return 'done'