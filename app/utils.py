from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash(password: str):
    hashed = pwd_context.hash(password)
    return hashed


def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)
