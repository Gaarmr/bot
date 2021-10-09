from telegram import ReplyKeyboardRemove, ReplyKeyboardMarkup

def quest_start(update, context):
    update.message.reply_text(
        "What is your name? Enter your first and last name",
        reply_markup=ReplyKeyboardRemove()
    )
    return "name"

def quest_name(update, context):
    user_name = update.message.text
    if len(user_name.split()) < 2:
        update.message.replt_text('Please, enter your first and last name')
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
        "Leave a free-form comment or skip this step by typing /skip"
    )
    return "comment"