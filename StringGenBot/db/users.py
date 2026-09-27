from StringGenBot.db import db

usersdb = db.users


async def is_served_user(user_id: int) -> bool:
    return await usersdb.find_one({"user_id": user_id}) is not None


async def get_served_users() -> list:
    return [user async for user in usersdb.find({"user_id": {"$gt": 0}})]


async def add_served_user(user_id: int):
    # Atomic insert avoids duplicate rows if /start and the user tracker run together.
    result = await usersdb.update_one({"user_id": user_id}, {"$setOnInsert": {"user_id": user_id}}, upsert=True)
    return result.upserted_id is not None
