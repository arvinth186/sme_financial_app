from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.deps import get_db
from app.models.user import User
from app.auth.security import hash_password, verify_password
from app.auth.jwt import create_access_token
from app.auth.security import hash_password
from app.schema.auth import UserRegister,UserLogin


"""
This file is used to store the authentication routes
It is used in the main.py file to store the authentication routes
"""

router = APIRouter(prefix="/auth", tags=["Authentication"])


# Register API
@router.post("/register")
def register_user(payload: UserRegister, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email).first()
    if user:
        raise HTTPException(status_code=400, detail="User already exists")

    new_user = User(
        email=payload.email,
        hashed_password=hash_password(payload.password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User registered successfully"}


# Login API

from app.schema.auth import UserLogin

@router.post("/login")
def login_user(payload: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email).first()

    if not user or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": str(user.id)})

    return {
        "access_token": token,
        "token_type": "bearer"
    }


