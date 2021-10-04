from emoji import emojize
from glob import glob
import logging
import settings
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from random import randint, choice

logging.basicConfig(filename='bot.log', level=logging.INFO)

gain=100

def play_dice(user_number, bet, gain):
    if user_number<2 or user_number>12:
        message = 'Number out of range. \nPlease enter a number from 2 to 12' 
    elif bet<1 or bet>gain:
        message = 'Bet is not allowed'
    else:
        score1 = randint(1,6)
        score2 = randint(1,6)
        total_score = score1 + score2
        if total_score==user_number:
            gain += 4 * bet
            message = f"На первом кубике выпало {score1}. На втором кубике выпало {score2}. \nВы выйграли : {bet}х4, ваш счет {gain}"
        elif total_score < 7 and user_number<7:
            gain += bet
            message = f"На первом кубике выпало {score1}. На втором кубике выпало {score2}. \nВы выйграли : {bet}, ваш счет {gain}"
        elif total_score > 7 and user_number>7:
            gain += bet
            message = f"На первом кубике выпало {score1}. На втором кубике выпало {score2}. \nВы выйграли : {bet}, ваш счет {gain}"
        else:
            gain -= bet
            message = f"На первом кубике выпало {score1}. На втором кубике выпало {score2}. \nСтавка проиграна, ваш счет {gain}"
    return message


def dice_number(update, context):
    print(context.args)
    if context.args:
        try: 
            user_number = int(context.args[0])
            bet = int(context.args[1])
            message = play_dice(user_number, bet, gain)
        except (TypeError, ValueError):
            message = 'Enter an integer'
    else:
        #update.message.reply_text(rules)
        message = '\nEnter an integer \nUse /dice #number# #bet#'
    update.message.reply_text(message)

def show_rules(update, context):
    pic_filename='telegrammbot\img\game_dice.png'
    chat_id = update.effective_chat.id
    context.bot.send_photo(chat_id=chat_id, photo=open(pic_filename, 'rb'))

def send_cat_picture(update, context):
    cat_photos_list = glob('telegrammbot\img\cat*.jp*g')
    cat_pic_filename = choice(cat_photos_list)
    chat_id = update.effective_chat.id
    context.bot.send_photo(chat_id=chat_id, photo=open(cat_pic_filename, 'rb'))

def get_smile(user_data):
    if 'emoji' not in user_data:
        smile = choice(settings.USER_EMOJI)
        return emojize(smile, use_aliases=True)
    return user_data['emoji']

def talk_to_me(update, context):
    smile = get_smile(context.user_data)
    username = update.effective_user.first_name
    user_text = update.message.text 
    update.message.reply_text(f"Hello!, {username} {smile}! You wrote: {user_text}")
    update.message.reply_text('Commands: /start /rules /dice /cat')

def greet_user(update, context):
    smile = get_smile(context.user_data)
    print('Вызван /start')
    update.message.reply_text(f'Hello! Commands: /start /rules /dice /cat {smile}')

def main():
    mybot = Updater(settings.API_KEY, use_context=True)
    dp = mybot.dispatcher
    dp.add_handler(CommandHandler('cat', send_cat_picture))
    dp.add_handler(CommandHandler('rules', show_rules))
    dp.add_handler(CommandHandler('dice', dice_number))
    dp.add_handler(CommandHandler("start", greet_user))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))

    logging.info("Bot is start")
    
    mybot.start_polling()
    mybot.idle()

if __name__ == "__main__":
    main()
