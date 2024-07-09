from fastapi import FastAPI
from pydantic import BaseModel, EmailStr

app = FastAPI()



class LoginIn(BaseModel):
    name: str
    email: EmailStr
    fpl_id: str
    password: str

class LoginOut(BaseModel):
    name:str
    email: EmailStr
    fpl_id: str

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/api/v1/login",response_model=LoginOut)
async def login(user:LoginIn):
    #DEFINE models later on.
    user=user.dict()
    return {"message": "Hello World"}

@app.post("/api/v1/register")
async def register():
    #DEFINE models later on.
    return {"message": "Hello World"}

@app.post("/api/v1/topup")
async def topup():
    #DEFINE models later on.
    return {"message": "Hello World"}

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