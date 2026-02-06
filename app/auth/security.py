from passlib.context import CryptContext

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

"""
This function is used to hash a password
It is used in the register route to hash a password
IT is also used to verify a password
"""

def hash_password(password: str) -> str:
    # safety guard
    if len(password.encode("utf-8")) > 72:
        password = password[:72]
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)    
