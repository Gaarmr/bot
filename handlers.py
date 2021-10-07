from glob import glob
from random import choice
from utils import main_keyboard, get_smile

def greet_user(update, context):
    context.user_data['emoji'] = get_smile(context.user_data)
    update.message.reply_text(
        f"Hello! Commands: /start /rules /dice /gain /cat {context.user_data['emoji']}!",
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

def send_cat_picture(update, context):
    cat_photos_list = glob('telegrammbot\img\cat*.jp*g')
    cat_pic_filename = choice(cat_photos_list)
    chat_id = update.effective_chat.id
    context.bot.send_photo(chat_id=chat_id, photo=open(cat_pic_filename, 'rb'))

def user_coordinates(update, context):
    context.user_data['emoji'] = get_smile(context.user_data)
    coords = update.message.location
    update.message.reply_text(
        f"Ваши координаты {coords} {context.user_data['emoji']}!",
    )