# import model
import env
import mongoModel
import responseModel
# import Motor
import motor.motor_asyncio
from fastapi import FastAPI  # import class FastAPI() từ thư viện fastapi
import os
from fastapi import FastAPI, Body, HTTPException, status, Header, Depends
from fastapi.security import OAuth2PasswordBearer
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from typing import Optional, List
from fastapi.middleware.cors import CORSMiddleware

# JWT
from jose import JWTError, jwt
SECRET_KEY = "bloblaahihi"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 600

# App
app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
client = motor.motor_asyncio.AsyncIOMotorClient(env.MONGODB_URL)
db = client.fastbook
app = FastAPI()  # gọi constructor và gán vào biến app
origins = [
    "https://localhost",
    "https://localhost:3000",
    "https://localhost:8000",
    "*"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# use model
UserModel = mongoModel.UserModel
UpdateUserModel = mongoModel.UpdateUserModel
AuthUserModel = mongoModel.AuthUserModel
TokenModel = responseModel.TokenModel

DEFAULT_AVATAR = "https://i.ibb.co/H4WHmsn/default-avatar.png"
# Function


def get_token(data: dict, secret: str = SECRET_KEY, algorithm: str = ALGORITHM):
    encoded_jwt = jwt.encode(data, secret, algorithm)
    return {
        "accessToken": encoded_jwt,
        "type": "Bearer"
    }


def decode_token(token, secret: str = SECRET_KEY, algorithm: str = ALGORITHM):
    decoded_jwt = jwt.decode(token, secret, algorithm)
    return decoded_jwt
# All API


@app.get("/api")  # giống flask, khai báo phương thức get và url
async def api():  # do dùng ASGI nên ở đây thêm async, nếu bên thứ 3 không hỗ trợ thì bỏ async đi
    return {
        "success": True,
        "message": "API",
        "API": {
            "allApi": "/api",
            "register": "/auth/register",
            "login": "/auth/login",
            "profile": "/me"
        }
    }


# Auth API


@app.post("/auth/register", response_description="Register new user")
async def auth_register(user: UserModel = Body(...)):
    user = jsonable_encoder(user)
    check_exist_user = await db["users"].find_one({"username": user["username"]})
    if (check_exist_user == None):
        default_avatar = "https://i.ibb.co/H4WHmsn/default-avatar.png"
        user |= {"avatar": default_avatar}
        new_user = await db["users"].insert_one(user)
        created_user = await db["users"].find_one({"_id": new_user.inserted_id})
        token_data = {
            "userId": str(created_user.get('_id')),
            "name": created_user["name"],
            "username": created_user["username"]
        }
        access_token = get_token(token_data)
        print(access_token)
        res = {
            "success": True,
            "message": "register successfull"
        }
    else:
        res = {
            "success": False,
            "message": "username invailid"
        }
    return res


@app.post("/auth/login", response_description="User login")
async def auth_login(login_user=Body(...)):
    login_user = jsonable_encoder(login_user)
    check_user = await db["users"].find_one({"username": login_user["username"]})
    # print(check_user.get('_id'))
    if (check_user == None):
        res = {
            "success": False,
            "message": "Error username"
        }
    elif (check_user["password"] != login_user["password"]):
        res = {
            "success": False,
            "message": "Error password"
        }
    else:
        user_id = str(check_user.get('_id'))
        avatar = check_user["avatar"]
        token_data = {
            "userId": user_id,
            "name": check_user["name"],
            "username": check_user["username"],
            "avatar": avatar,
        }
        access_token = get_token(token_data)
        res = {
            "success": True,
            "userData": {
                "userId": user_id,
                "name": check_user["name"],
                "username": check_user["username"],
                "avatar": avatar
            }
        } | access_token
    return res

# User API


@app.get("/me", response_description="User data")
async def get_user_profile(token: str = Depends(oauth2_scheme)):
    payload = decode_token(token)
    print(payload)
    return payload


# Get data from ID
@app.get("/users/{userId}", response_description="User data with id")
async def read_item(userId: str):
    print(userId)
    check_user = await db["users"].find_one({"_id": userId})
    if (check_user == None):
        res = {
            "success": False,
            "message": "Not Found"
        }
    else:
        res = {
            "success": True,
            "userId": str(check_user.get('_id')),
            "name": check_user["name"],
            "username": check_user["username"]
        }
    return res

# TEST
# Newfeed API


@app.get("/posts", response_description="Get post at new feed")
async def list_posts():
    # posts = await db["posts"].find().to_list(10)
    posts = []
    res = {
        "success": True,
        "posts": [
            {
                "postId": "pid01",
                "reactedUsers": [
                    "uid01",
                    "uid02",
                    "uid03"
                ],
                "user": {
                    "userId": "2",
                    "name": "Lady Gaga",
                    "avatar": "https://sre.vn/wp-content/uploads/2020/12/lady-gaga-lan-san-dien-anh-trong-bo-phim-hanh-dong-moi-lady.jpg"
                },
                "content": {
                    "value": "Hello, My name is Lady Gaga!",
                    "image":
                    "https://znews-photo.zadn.vn/w660/Uploaded/rohunwa/2019_03_29/lady_gaga_11_1_thumb.jpg",
                    "time": "just now",
                },
                "reactions": {
                    "likes": 321,
                    "comments": 23,
                },
            },
            {
                "postId": "pid02",
                "reactedUsers": [
                    "uid01",
                    "uid02",
                    "uid03"
                ],
                "user": {
                    "userId": "4",
                    "name": "Spider Man",
                    "avatar": "https://comicvine.gamespot.com/a/uploads/scale_super/12/126309/5030561-0452253614-latest"
                },
                "content": {
                    "value": "Hello, I am Spider Man!",
                    "image":
                    "https://img.hulu.com/user/v3/artwork/f82b95f5-13da-4acd-b378-7d3f6864919f?base_image_bucket_name=image_manager&base_image=4b2d95d2-c41b-4ed2-b9d1-cc0f8f80e0a2&region=US&format=jpeg&size=952x536",
                    "time": "2hrs ago",
                },
                "reactions": {
                    "likes": 1,
                    "comments": 0,
                },
            },
        ]
    }
    return res


@app.post("/posts/create", response_description="create new post from user")
async def create_new_post(newPost=Body(...), token: str = Depends(oauth2_scheme)):
    # print(token)
    payload = decode_token(token)
    check_user_id = payload["userId"] == newPost["user"]["userId"]
    res = {
        "success": check_user_id,
        "message": check_user_id and "Posted" or "Unauthentication",
    }
    return res


# Test


@app.get(
    "/", response_description="List all users", response_model=List[UserModel]
)
async def list_users():
    users = await db["users"].find().to_list(10)
    return users
