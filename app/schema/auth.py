from pydantic import BaseModel, EmailStr

"""
This class is used to store the user registration information
It is used in the auth/routes.py file to store the user registration information
"""
class UserRegister(BaseModel):
    email: EmailStr
    password: str

"""
This class is used to store the user login information
It is used in the auth/routes.py file to store the user login information
"""
class UserLogin(BaseModel):
    email: EmailStr
    password: str

