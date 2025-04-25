from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from services import user_service
from schemas import schemas,apiResponse
from datetime import datetime

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=apiResponse.APIResponseBase)
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = user_service.get_users_service(db, skip=skip, limit=limit)
    users_response = [schemas.UserResponse.from_orm(user) for user in users]

    return apiResponse.APIResponseBase(
        status="success",
        data=users_response,
        timeStamp=datetime.now()
    )

@router.get("/{id}", response_model=apiResponse.APIResponseBase)
def get_user_by_id(id: int, db: Session = Depends(get_db)):
    try:
        user = user_service.get_users_by_id(db, id)

        user_response = schemas.UserResponse.from_orm(user)

        return apiResponse.APIResponseBase(
        status="success",
        data=user_response,
        timeStamp=datetime.now()
    )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    

@router.post("/", response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    try:
        return user_service.create_user_service(db, user)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/{id}", response_model=schemas.UserResponse)
def update_user(id: int, user: schemas.UserCreate, db: Session = Depends(get_db)):
    try:
        return user_service.update_user_service(db, id, user)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.delete("/{id}", response_model=apiResponse.APIResponseBase)
def delete_user(id: int, db: Session = Depends(get_db)):
    try:
        user = user_service.delete_user_service(db, id)

        return apiResponse.APIResponseBase(
        status="success",
        data={"id": id},
        timeStamp=datetime.now()
    )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

