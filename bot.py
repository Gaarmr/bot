from dice import dice_number, get_gain, show_rules
from handlers import check_user_photo, greet_user, send_picture, talk_to_me, user_coordinates
import logging
from questionnaire import quest_start, quest_name, quest_rate, quest_skip, quest_comment, quest_dontknow
import settings
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler

logging.basicConfig(filename='bot.log', level=logging.INFO)

def main():
    mybot = Updater(settings.API_KEY, use_context=True)
    
    dp = mybot.dispatcher

    questionnaire = ConversationHandler(
        entry_points=[MessageHandler(Filters.regex('^(Questionnaire)$'), quest_start)],
        states={
            "name": [MessageHandler(Filters.text, quest_name)],
            "rating": [MessageHandler(Filters.regex('^(1|2|3|4|5)$'), quest_rate)],
            "comment": [
                CommandHandler('skip', quest_skip),
                MessageHandler(Filters.text | Filters.video | Filters.photo | Filters.document| Filters.location, quest_comment)
            ]
        },
        fallbacks=[
            MessageHandler(Filters.text, quest_dontknow)
        ] 
    )

    dp.add_handler(questionnaire)
    dp.add_handler(CommandHandler('pic', send_picture))
    dp.add_handler(CommandHandler('rules', show_rules))
    dp.add_handler(CommandHandler('gain', get_gain))
    dp.add_handler(CommandHandler('dice', dice_number))
    dp.add_handler(CommandHandler('start', greet_user))
    dp.add_handler(MessageHandler(Filters.regex('^(Pic)$'), send_picture))
    dp.add_handler(MessageHandler(Filters.regex('^(Gain)$'), get_gain))
    dp.add_handler(MessageHandler(Filters.regex('^(Dice)$'), dice_number))
    dp.add_handler(MessageHandler(Filters.regex('^(Rules)$'), show_rules))
    dp.add_handler(MessageHandler(Filters.regex('^(Start)$'), greet_user))
    dp.add_handler(MessageHandler(Filters.photo, check_user_photo))
    dp.add_handler(MessageHandler(Filters.location, user_coordinates))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))

    logging.info('Bot is start')
   
    mybot.start_polling()
    mybot.idle()

if __name__ == "__main__":
    main()