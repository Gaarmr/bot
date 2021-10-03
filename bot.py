from rules_eng import rules
import settings
import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from random import randint

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
    update.message.reply_text(rules)

def talk_to_me(update, context):
    user_text = update.message.text 
    print(user_text)
    update.message.reply_text(user_text)
    update.message.reply_text('Hello! Commands: /start /rules /dice')

def greet_user(update, context):
    print('Вызван /start')
    update.message.reply_text('Hello! Commands: /start /rules /dice')

def main():
    mybot = Updater(settings.API_KEY, use_context=True)
    dp = mybot.dispatcher
    dp.add_handler(CommandHandler('rules', show_rules))
    dp.add_handler(CommandHandler('dice', dice_number))
    dp.add_handler(CommandHandler("start", greet_user))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))

    logging.info("Bot is start")
    
    mybot.start_polling()
    mybot.idle()

if __name__ == "__main__":
    main()
