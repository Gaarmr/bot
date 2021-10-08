from clarifai.rest import ClarifaiApp
from emoji import emojize
from pprint import PrettyPrinter
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

def is_cat(file_name):
    app = ClarifaiApp(api_key=settings.CLARIFAI_API_KEY)
    model = app.public_models.general_model
    response = model.predict_by_filename(file_name, max_concepts=5)
    return response

is_cat("img\pic_4.jpg")
'''
if __name__ == "__main__":
        response = is_cat("img\pic_3.jpg")
        print(response)
'''