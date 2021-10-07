from emoji import emojize
from random import choice
import settings
from telegram import ReplyKeyboardMarkup, KeyboardButton

def main_keyboard():
    return ReplyKeyboardMarkup([
        ['Start'], 
        ['Rules', 'Dice', 'Gain'],
        ['Pic'],
        [KeyboardButton('Location', request_location=True)]
        ])

def get_smile(user_data):
    if 'emoji' not in user_data:
        smile = choice(settings.USER_EMOJI)
        return emojize(smile, use_aliases=True)
    return user_data['emoji']