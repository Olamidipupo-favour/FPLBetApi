from fastapi import FastAPI,Depends, HTTPException, status, Header
from pydantic import BaseModel, EmailStr
from typing import Any, Union, Annotated
from crontab import CronTab
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import jwt
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from bson.objectid import ObjectId


SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1000


class LoginIn(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    email: EmailStr
    token: str


class RegisterOut(BaseModel):
    name: str
    email: EmailStr
    fpl_id: str
class RegisterIn(LoginIn):
    name: str
    fpl_id: str
class UserInDb(BaseModel):
    name: str
    email: EmailStr
    fpl_id: str
    _id: str

class TokenData(BaseModel):
    email: str
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(Authorization: Annotated[str, Header()]) -> Union[UserInDb, None]:  # Union[UserInDB, None] (Union[UserInDB, None] means None can be returned from get_current_user function.) -> Union[UserInDB, None] (Union[UserInDB, None] means None can be returned from get_current_user function.str):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    token=Authorization.split()[1]
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except InvalidTokenError:
        raise credentials_exception
    user = client.BetTest.bet.users.find_one({"email": token_data.email})
    user['id']=str(user['_id'])
    user = UserInDb(**user)
    if user is None:
        raise credentials_exception
    return user


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

app = FastAPI()
cron = CronTab(user=True)
#job = cron.new(command='python path/to/your_script.py')
#job.minute.every(1)

uri = "mongodb+srv://akinlua:propTest@cluster0.zocymky.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(uri, server_api=ServerApi('1'))
@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/api/v1/login")
async def login(user:LoginIn) -> Any:
    #DEFINE models later on.
    #push data to db
    user_=client.BetTest.bet.users.find_one({"email": user.email})
    if(pwd_context.verify(user.password,user_["password"])):
        return Token(email=user.email,token=create_access_token({"sub": user.email}))
    else:
        return {"message": "Wrong Password"},status.HTTP_401_UNAUTHORIZED

@app.post("/api/v1/register",response_model=RegisterOut)
async def register(user:RegisterIn) -> Any:
    #DEFINE models later on.
    user_in_db = {"name": user.name, "email": user.email, "fpl_id": user.fpl_id, "password": pwd_context.hash(user.password)}
    #push data to db
    client.BetTest.bet.users.insert_one(user_in_db)
    return user

@app.post("/api/v1/topup")
async def topup():
    return {"message": "Hello World"}

@app.get("/api/v1/user")
async def get_users(current_user:Annotated[UserInDb, Depends(get_current_user)]):
    #DEFINE models later on.
    return current_user

@app.get("/api/v1/users")
async def get_users():
    #DEFINE models later on.
    return {"message": "Hello World"}

@app.get("/api/v1/users/{user_id}")
async def get_user(user_id:str):
    #DEFINE models later on.
    return {"message": "Hello World"}

@app.post("/api/v1/bet")
async def bet():
    #DEFINE models later on.
    return {"message": "Hello World"}

@app.get("/api/v1/bets")
async def get_bets():
    #DEFINE models later on.
    return {"message": "Hello World"}

@app.get("/api/v1/bets/{bet_id}")
async def get_bet(bet_id:str):
    #DEFINE models later on.
    return {"message": "Hello World"}

@app.get("/api/v1/balance")
async def get_balance():
    #DEFINE models later on.
    return {"message": "Hello World"}