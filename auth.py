from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from security import decode_token

# OAuth2PasswordBearer คือ dependency ที่จะดึง token จาก request
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# ฟังก์ชันสำหรับตรวจสอบ JWT token
def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = decode_token(token)
    if payload is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    return payload
