from glob import glob
import os
from random import choice
from utils import main_keyboard, get_smile

def greet_user(update, context):
    context.user_data['emoji'] = get_smile(context.user_data)
    update.message.reply_text(
        f"Hello! Commands: /start /rules /dice /gain /pic {context.user_data['emoji']}!",
        reply_markup = main_keyboard()
        )

def talk_to_me(update, context):
    context.user_data['emoji'] = get_smile(context.user_data)
    username = update.effective_user.first_name
    user_text = update.message.text 
    update.message.reply_text(
        f"Hello!, {username} {context.user_data['emoji']}! You wrote: {user_text} \nUse /start",
        reply_markup = main_keyboard()
        )

def send_picture(update, context):
    photos_list = glob('img\pic*.*')
    pic_filename = choice(photos_list)
    chat_id = update.effective_chat.id
    context.bot.send_photo(chat_id=chat_id, photo=open(pic_filename, 'rb'))

def user_coordinates(update, context):
    context.user_data['emoji'] = get_smile(context.user_data)
    coords = update.message.location
    update.message.reply_text(
        f"Ваши координаты {coords} {context.user_data['emoji']}!",
    )

def check_user_photo(update, context):
    update.message.reply_text('Processing the photo')
    os.makedirs('downloads', exist_ok=True)
    user_photo = context.bot.getFile(update.message.photo[-1].file_id)
    file_name = os.path.join("downloads", f"{user_photo.file_id}.jpg")
    user_photo.download(file_name)
    update.message.reply_text('Your photo is saved')