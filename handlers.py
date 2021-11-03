from db import db, get_or_create_user
from glob import glob
import os
from random import choice
from utils import is_cat, main_keyboard

def greet_user(update, context):
    user = get_or_create_user(db, update.effective_user, update.message.chat_id)
    update.message.reply_text(
        f"Hello! Commands: /start /rules /dice /gain /pic {user['emoji']}!",
        reply_markup = main_keyboard()
        )


def talk_to_me(update, context):
    user = get_or_create_user(db, update.effective_user, update.message.chat_id)
    username = update.effective_user.first_name
    user_text = update.message.text 
    update.message.reply_text(
        f"Hello!, {username} {user['emoji']}! You wrote: {user_text} \nUse /start",
        reply_markup=main_keyboard()
        )


def send_picture(update, context):
    photos_list = glob('img\pic*.*')
    pic_filename = choice(photos_list)
    chat_id = update.effective_chat.id
    context.bot.send_photo(chat_id=chat_id, photo=open(pic_filename, 'rb'))


def user_coordinates(update, context):
    user = get_or_create_user(db, update.effective_user, update.message.chat_id)
    coords = update.message.location
    update.message.reply_text(
        f"Ваши координаты {coords} {user['emoji']}!",
    )


def check_user_photo(update, context):
    update.message.reply_text('Processing the photo')
    user_photo = context.bot.getFile(update.message.photo[-1].file_id)
    url_file_path = user_photo.file_path
    if is_cat(url_file_path):
        update.message.reply_text('Cat is detected, saved photo')
        os.makedirs('downloads', exist_ok=True)
        file_name = os.path.join("img", f"pic_{user_photo.file_id}.jpg")
        user_photo.download(file_name)
    else:
        update.message.reply_text('Cat is not detected, delete photo')