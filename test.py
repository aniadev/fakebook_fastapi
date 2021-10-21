# JWT
from jose import JWTError, jwt
SECRET_KEY = "bloblaahihi"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
data = {
    "userId": "234234j23h423kjb5k12jk3h12jk4",
    "timeExpires": ACCESS_TOKEN_EXPIRE_MINUTES,
    "username": "phamhai8599"
}
encoded_jwt = jwt.encode(data,
                         SECRET_KEY, algorithm=ALGORITHM)
print(encoded_jwt)
try:
    decoded_value = jwt.decode(encoded_jwt, SECRET_KEY, algorithms=ALGORITHM)
    print(decoded_value)
except JWTError:
    print("Error decoded")
