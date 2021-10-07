from dice import dice_number, get_gain, show_rules
from handlers import greet_user, send_picture, talk_to_me, user_coordinates
import logging
import settings
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

logging.basicConfig(filename='bot.log', level=logging.INFO)

def main():
    mybot = Updater(settings.API_KEY, use_context=True)
    
    dp = mybot.dispatcher

    dp.add_handler(CommandHandler('pic', send_picture))
    dp.add_handler(CommandHandler('rules', show_rules))
    dp.add_handler(CommandHandler('gain', get_gain))
    dp.add_handler(CommandHandler('dice', dice_number))
    dp.add_handler(CommandHandler("start", greet_user))
    dp.add_handler(MessageHandler(Filters.regex('^(Pic)$'), send_picture))
    dp.add_handler(MessageHandler(Filters.regex('^(Gain)$'), get_gain))
    dp.add_handler(MessageHandler(Filters.regex('^(Dice)$'), dice_number))
    dp.add_handler(MessageHandler(Filters.regex('^(Rules)$'), show_rules))
    dp.add_handler(MessageHandler(Filters.regex('^(Start)$'), greet_user))
    dp.add_handler(MessageHandler(Filters.location, user_coordinates))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))

    logging.info("Bot is start")
   
    mybot.start_polling()
    mybot.idle()

if __name__ == "__main__":
    main()