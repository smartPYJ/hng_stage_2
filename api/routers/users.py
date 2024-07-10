from .. import models, schemas, utils, oauth
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from ..database import get_db
from sqlalchemy.orm import Session
from fastapi import Depends, status, APIRouter, HTTPException
import uuid
from typing import List

router = APIRouter()


@router.post(
    "/auth/register",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.RegisterResponseSchema,
)
def create_user(user: schemas.CreateUser, db: Session = Depends(get_db)):
    try:
        hash_password = utils.hash(user.password)
        user.password = hash_password
        new_user = models.User(**user.model_dump())

        organisation = models.Organisation(
            org_id=str(uuid.uuid4()),
            name=(user.firstName + "'s" + " Organisation"),
            description="",
            user_id=new_user.userId,
        )

        db.add(new_user)
        db.add(organisation)

        db.commit()
        db.refresh(new_user)
        db.refresh(organisation)

        new_association = models.User_Org_Ass(
            user_id=new_user.userId, organization_id=organisation.org_id
        )
        db.add(new_association)
        db.commit()
        return_user = {
            "status": "success",
            "message": "Registration successful",
            "data": {
                "accessToken": "we",  # Placeholder for actual token
                "user": {
                    "userId": str(new_user.userId),
                    "firstName": new_user.firstName,
                    "lastName": new_user.lastName,
                    "email": new_user.email,
                    "phone": new_user.phone,
                },
            },
        }
        return return_user
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "status": "Bad request",
                "message": "Registration unsuccessful",
                "statusCode": 400,
            },
        )


@router.get("/api/users/{id}", response_model=schemas.RegisterResponseSchema)
def get_users(id: str, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.userId == id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"user with {id} does not exist",
        )
    return_user = {
        "status": "success",
        "message": "Query successful",
        "data": {
            "user": {
                "userId": str(user.userId),
                "firstName": user.firstName,
                "lastName": user.lastName,
                "email": user.email,
                "phone": user.phone,
            },
        },
    }
    return return_user


@router.post(
    "/auth/login",
    response_model=schemas.RegisterResponseSchema,
    status_code=status.HTTP_401_UNAUTHORIZED,
)
def user_login(
    user_credential: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):

    user = (
        db.query(models.User)
        .filter(models.User.email == user_credential.username)
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "status": "Bad request",
                "message": "Authentication failed",
                "statusCode": 401,
            },
        )
    if not utils.verify(user_credential.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "status": "Bad request",
                "message": "Authentication failed",
                "statusCode": 401,
            },
        )

    access_token = oauth.create_access_token(
        data={"userId": user.userId, "firstName": user.firstName}
    )
    return_user = {
        "status": "success",
        "message": "login successful",
        "data": {
            "accessToken": access_token,  # Placeholder for actual token
            "user": {
                "userId": str(user.userId),
                "firstName": user.firstName,
                "lastName": user.lastName,
                "email": user.email,
                "phone": user.phone,
            },
        },
    }
    return return_user


@router.get(
    "/api/organisations",
    status_code=status.HTTP_200_OK,
    response_model=List[schemas.OrganisationR],
)
def get_post(
    db: Session = Depends(get_db),
    user_id: str = Depends(oauth.get_current_user)
):

    org = (
        db.query(models.Organisation)
        .filter(models.Organisation.user_id == user_id.userId)
        .all()
    )

    return org


@router.post(
    "/api/organisations",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.OrganisationResponse,
)
def create_org(
    org: schemas.Organisation,
    db: Session = Depends(get_db),
    user_id: str = Depends(oauth.get_current_user),
):
    try:
        id = str(uuid.uuid4())
        user = user_id.userId
        new_org = models.Organisation(**org.model_dump(),
                                      user_id=user, org_id=id)
        print(new_org)

        db.add(new_org)
        db.commit()

        db.refresh(new_org)

        new_association = models.User_Org_Ass(
            user_id=user_id.userId, organization_id=new_org.org_id
        )
        db.add(new_association)
        db.commit()
        return_user = {
            "status": "success",
            "message": "Registration successful",
            "data": {
                "org_Id": str(new_org.org_id),
                "name": new_org.name,
                "description": new_org.description,
            },
        }
        return return_user
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "status": "Bad request",
                "message": "Registration unsuccessful",
                "statusCode": 400,
            },
        )


@router.get(
    "/api/organisations/{id}",
    status_code=status.HTTP_200_OK,
    response_model=schemas.OrganisationResponse,
)
def get_one_org(
    id: str,
    db: Session = Depends(get_db),
    user_id: str = Depends(oauth.get_current_user),
):
    try:

        org = (
            db.query(models.Organisation)
            .filter(models.Organisation.org_id == id)
            .first()
        )

        return_org = {
            "status": "success",
            "message": "Fetch Successful",
            "data": {
                "org_Id": str(org.org_id),
                "name": org.name,
                "description": org.description,
            },
        }
        return return_org
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "status": "Bad request",
                "message": "Fetch unsuccessful",
                "statusCode": 400,
            },
        )
