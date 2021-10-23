from db import db, get_or_create_user, save_quest
from telegram import ParseMode, ReplyKeyboardRemove, ReplyKeyboardMarkup
from telegram.ext.conversationhandler import ConversationHandler
from utils import main_keyboard

def quest_start(update, context):
    update.message.reply_text(
        "What is your name? Enter your first and last name",
        reply_markup=ReplyKeyboardRemove()
    )
    return "name"

def quest_name(update, context):
    user_name = update.message.text
    if len(user_name.split()) < 2:
        update.message.reply_text('Please, enter your first and last name')
        return 'name'
    else:
        context.user_data['quest'] = {'name': user_name}
        reply_keyboard = [['1', '2', '3', '4', '5']]
        update.message.reply_text(
            'Rate the bot on a scale of 1 to 5',
            reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
        )
        return 'rating'

def quest_rate(update, context):
    context.user_data["quest"]["rating"] = int(update.message.text)
    update.message.reply_text(
        "Enter a free-form comment or skip this step by typing /skip"
    )
    return "comment"

def quest_comment(update, context):
    context.user_data['quest']['comment'] = update.message.text
    user = get_or_create_user(db, update.effective_user, update.message.chat_id)
    save_quest(user['user_id'], context.user_data['quest'])
    user_text = format_quest(context.user_data['quest'])
    update.message.reply_text(user_text, reply_markup=main_keyboard(), parse_mode=ParseMode.HTML)
    return ConversationHandler.END

def quest_skip(update, context):
    user_text = format_quest(context.user_data['quest'])
    user = get_or_create_user(db, update.effective_user, update.message.chat_id)
    save_quest(user['user_id'], context.user_data['quest'])
    update.message.reply_text(user_text, reply_markup=main_keyboard(), parse_mode=ParseMode.HTML)
    return ConversationHandler.END


def format_quest(quest):
    user_text = f"""
<b>Name</b>: {quest['name']}
<b>Rate</b>: {quest['rating']}
"""
    if 'comment' in quest:
        user_text += f"\n<b>Comment</b>: {quest['comment']}"
    return user_text


def quest_dontknow(update, context):
    update.message.reply_text('Please, rate the bot on a scale of 1 to 5')