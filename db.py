from emoji import emojize
from datetime import datetime
from pymongo import MongoClient
from random import choice
import settings

client = MongoClient(settings.MONGO_LINK)

db = client[settings.MONGO_DB]


def get_or_create_user(db, effective_user, chat_id):
    user = db.users.find_one({"user_id": effective_user.id})
    if not user:
        user = {
            "user_id": effective_user.id,
            "first_name": effective_user.first_name,
            "last_name": effective_user.last_name,
            "username": effective_user.username,
            "chat_id": chat_id,
            "emoji": emojize(choice(settings.USER_EMOJI), use_aliases=True)
        }
        db.users.insert_one(user)
    return user


def save_quest(user_id, quest_data):
    user = db.users.find_one({'user_id': user_id})
    quest_data['created'] = datetime.now()
    if 'quest' not in user:
        db.users.update_one(
            {'_id': user['_id']},
            {'$set': {'quest': [quest_data]}}
        )
    else:
        db.users.update_one(
            {'_id': user['_id']},
            {'$push': {'quest': quest_data}}
        )
