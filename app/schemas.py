from typing import Optional
from pydantic import BaseModel, EmailStr


class CreateUser(BaseModel):
    userId: str
    firstName: str
    lastName: str
    email: EmailStr
    password: str
    phone: str


class ReturnUser(BaseModel):

    userId: str
    firstName: str
    lastName: str
    email: EmailStr
    phone: str

    class Config:
        orm_mode = True


class ResponseModel(BaseModel):
    status: str
    message: str
    data: dict


class UserSchema(BaseModel):
    userId: Optional[str]
    firstName: Optional[str]
    lastName: Optional[str]
    email: EmailStr
    phone: Optional[str]


class RegisterResponseSchema(BaseModel):
    status: str
    message: str
    data: dict[str, str | UserSchema]


class Organisation(BaseModel):

    name: str
    description: str


class OrganisationR(BaseModel):
    org_id: str
    name: str
    description: str


class OrganisationResponse(BaseModel):
    status: str
    message: str
    data: dict[str, str | Organisation]


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    userId: str
    firstName: str
