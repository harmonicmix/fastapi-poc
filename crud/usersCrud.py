from sqlalchemy.orm import Session
from fastapi import HTTPException
import models.models as models, schemas.schemas as schemas

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).order_by(models.User.id).offset(skip).limit(limit).all()

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(name=user.name, email=user.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_id(db: Session, id: int):
    return db.query(models.User).filter(models.User.id == id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def update_user(db: Session, id: int, user: schemas.UserCreate):
    try:
        db_user = db.query(models.User).filter(models.User.id == id).first()
        if not db_user:
            raise HTTPException(status_code=404, detail="User not found")

        db_user.email = user.email
        db_user.name = user.name

        db.commit()

        return db_user

    except HTTPException as e:
        db.rollback()
        raise e

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Update failed: {str(e)}")


def delete_user(db: Session, user_id: int):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user:
        db.delete(db_user)
        db.commit()
    return db_user
