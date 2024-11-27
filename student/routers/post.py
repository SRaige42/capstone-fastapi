from .. import models, schemas
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import get_db
from .. import List

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)

@router.get("/", response_model=List[schemas.Post])
def get_post(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts

@router.post("/", status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends[get_db]):
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.get("/{ID}", response_model=schemas.Post)
def get_post(ID: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.ID == ID).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {ID} was not found")
    return post

@router.delete("/{ID}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(ID: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.ID == ID)
    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {ID} does not exist")
    post.delete(synchronize_session=False)
    db.commit()
    return Response (status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{ID}", response_model=schemas.Post)
def update_post(ID: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.ID == ID)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail=f"post with id: {ID} does not exist")
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()
