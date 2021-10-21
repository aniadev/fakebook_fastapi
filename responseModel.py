from pydantic import BaseModel


class TokenModel(BaseModel):
    access_token: str
    type: str
