from schemas import  schemas
from crud import usersCrud
from sqlalchemy.orm import Session

def create_user_service(db: Session, user: schemas.UserCreate):
    if len(user.email) < 5:
        raise ValueError("Email should be at least 5 characters long.")
    
    db_user = usersCrud.get_user_by_email(db, user.email)
    if db_user:
        raise ValueError("This Email is already registered")
    
    # ส่งข้อมูลให้ CRUD ทำงาน
    return usersCrud.create_user(db, user)

def get_users_service(db: Session, skip: int = 0, limit: int = 100):
    # Business logic เพิ่มเติม เช่น การจัดการ pagination หรือ query logic
    return usersCrud.get_users(db, skip=skip, limit=limit)

def get_users_by_id(db: Session, id: int):
    # Business logic เพิ่มเติม เช่น การจัดการ pagination หรือ query logic
    return usersCrud.get_user_by_id(db, id)

def update_user_service(db: Session, id: int, user: schemas.UserCreate):
    # ตรวจสอบว่า user ที่ต้องการอัพเดตมีอยู่ในฐานข้อมูลหรือไม่
    db_user = usersCrud.get_user_by_id(db, id)
    if not db_user:
        raise ValueError("User not found")
    
    # อัพเดตข้อมูลในฐานข้อมูล
    return usersCrud.update_user(db, id, user)

def delete_user_service(db: Session, id: int):
    db_user = usersCrud.get_user_by_id(db, id)
    if not db_user:
        raise ValueError("User not found")
    return usersCrud.delete_user(db, id)
