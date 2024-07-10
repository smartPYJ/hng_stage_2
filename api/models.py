from sqlalchemy import Column, String, ForeignKey
from .database import Base
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "users"

    userId = Column(String, primary_key=True, nullable=False, unique=True)
    firstName = Column(String, nullable=False)
    lastName = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    phone = Column(String)


class Organisation(Base):
    __tablename__ = "organisation"

    org_id = Column(String, nullable=False, primary_key=True, unique=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    user_id = Column(String, ForeignKey("users.userId"), nullable=False)

    user = relationship("User", backref="organisations")


class User_Org_Ass(Base):
    __tablename__ = "UserOrg"

    user_id = Column(String, ForeignKey("users.userId"), primary_key=True)
    organization_id = Column(
        String, ForeignKey("organisation.org_id"), primary_key=True
    )
