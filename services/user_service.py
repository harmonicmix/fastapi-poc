from fastapi import HTTPException
from schemas import  schemas
from crud import usersCrud
from sqlalchemy.orm import Session
import models.models as models

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


def transfer_money(db: Session, from_account_id: int, to_account_id: int, amount: float):
    try:
        # หา account A
        from_account = db.query(models.User).filter(models.User.id == from_account_id).first()
        if not from_account:
            raise HTTPException(status_code=404, detail="Sender account not found")

        # หา account B
        to_account = db.query(models.User).filter(models.User.id == to_account_id).first()
        if not to_account:
            raise HTTPException(status_code=404, detail="Recipient account not found")

        # เช็คเงินในบัญชี A
        if from_account.balance < amount:
            raise HTTPException(status_code=400, detail="Insufficient funds")

        # โอนเงิน: หัก A เพิ่ม B
        from_account.balance -= amount
        to_account.balance += amount

        # commit transaction
        db.commit()

        return {"message": f"Transferred {amount} successfully"}

    except HTTPException as e:
        db.rollback()
        raise e

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Transfer failed: {str(e)}")