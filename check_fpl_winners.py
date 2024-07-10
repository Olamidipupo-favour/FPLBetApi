import requests
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime
from bson.objectid import ObjectId

# Configuration
MONGO_URI = "mongodb+srv://akinlua:propTest@cluster0.zocymky.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
DB_NAME = "BetTest"
COLLECTION_NAME = "bet"

# MongoDB connection
client = AsyncIOMotorClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

# Season start date
season_start_date = datetime(2023, 8, 11)

def get_gameweek(season_start_date, season_current_date):
    days_since_start = (season_current_date - season_start_date).days
    gameweek = (days_since_start // 7) + 1
    if gameweek > 38:
        gameweek = 38
    return gameweek

async def fetch_fpl_data(fpl_id):
    FPL_API_URL = f"https://fantasy.premierleague.com/api/entry/{fpl_id}/history/"
    response = requests.get(FPL_API_URL)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch data for FPL ID {fpl_id}")
        return None

def calculate_gameweek_score(fpl_data, gameweek):
    for gw in fpl_data['current']:
        if gw['event'] == gameweek:
            return gw['points']
    return 0

async def check_fpl_winners():
    bets = await collection.find({"in_bet": True}).to_list(length=None)
    
    for bet in bets:
        user_id = bet["user_id"]
        with_ = bet["with_"]
        current_gameweek = get_gameweek(season_start_date, bet['date'])
        
        # Retrieve the points for both the user-id and with_
        user = await db.users.find_one({"_id": ObjectId(user_id)})
        with_user = await db.users.find_one({"_id": ObjectId(with_)})
        
        fpl_user_id = user.get("fpl_id")
        fpl_with_id = with_user.get("fpl_id")
        
        fpl_user_data = await fetch_fpl_data(fpl_user_id)
        fpl_with_data = await fetch_fpl_data(fpl_with_id)
        
        if fpl_user_data and fpl_with_data:
            user_score = calculate_gameweek_score(fpl_user_data, current_gameweek)
            with_score = calculate_gameweek_score(fpl_with_data, current_gameweek)
            
            if user_score > with_score:
                print("User wins the bet")
                await collection.update_one({"_id": ObjectId(bet['_id'])}, {"$set": {"in_bet": False}})
                await db.users.update_one({"_id": ObjectId(user_id)}, {"$inc": {"balance": bet["amount"]}})
            elif user_score < with_score:
                print("With wins the bet")
                await collection.update_one({"_id": ObjectId(bet['_id'])}, {"$set": {"in_bet": False}})
                await db.users.update_one({"_id": ObjectId(with_)}, {"$inc": {"balance": bet["amount"]}})
            else:
                print("Tie")
                await collection.update_one({"_id": ObjectId(bet['_id'])}, {"$set": {"in_bet": False}})
            # Store the result in the database or take further action

if __name__ == "__main__":
    import asyncio
    asyncio.run(check_fpl_winners())
