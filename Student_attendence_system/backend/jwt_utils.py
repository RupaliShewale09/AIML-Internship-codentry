from jose import jwt, JWTError
from datetime import datetime, timedelta
from fastapi import Depends, Header, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from backend.config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/admin/login")

def create_admin_token():
    payload = {
        "sub": "admin",
        "role": "admin",
        "exp": datetime.utcnow() + timedelta(
            minutes=settings.JWT_EXPIRE_MINUTES
        )
    }

    token = jwt.encode(
        payload,
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM
    )
    return token


def verify_admin_jwt(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM]
        )

        role = payload.get("role")

        if role != "admin":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Admin access required"
            )

        return payload

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired or invalid"
        )
