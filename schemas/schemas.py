from pydantic import BaseModel

class UserBase(BaseModel):
    name: str
    email: str
    balance: float
    class Config:
        from_attributes = True
        
class UserCreate(UserBase):
    pass

class UserResponse(UserBase):
    id: int

    class Config:
        from_attributes = True
