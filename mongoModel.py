from pydantic import BaseModel, Field, EmailStr
from bson import ObjectId
from typing import Optional, List


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


class UserModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    name: str = Field(...)
    username: str = Field(...)
    email: Optional[EmailStr]
    password: str = Field(...)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "name": "Jane Doe",
                "username": "Jane Doe",
                "email": "jdoe@example.com",
                "password": "123abc",
            }
        }


class UpdateUserModel(BaseModel):
    name: Optional[str]
    username: Optional[str]
    email: Optional[EmailStr]
    password: Optional[str]

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "name": "Jane Doe",
                "username": "Jane Doe",
                "email": "jdoe@example.com",
                "password": "123abc",
            }
        }


class AuthUserModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    name: Optional[str]
    username: Optional[str]
    email: Optional[EmailStr]

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "_id": "123b12v4h124vjn6",
                "name": "Jane Doe",
                "username": "Jane Doe",
                "email": "jdoe@example.com",
            }
        }
