import settings
import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, commandhandler

logging.basicConfig(filename='bot.log', level=logging.INFO)

def guess_number(update, context):
    print(context.args)
    if context.args:
        try: 
            user_number = int(context.args[0])
            message = f"Let's go. Your number is {user_number}"
        except (TypeError, ValueError):
            message = 'Enter an integer'
    else:
        message = 'Enter an integer \nUse /guess #number#'
    update.message.reply_text(message)

def talk_to_me(update, context):
    user_text = update.message.text 
    print(user_text)
    update.message.reply_text(user_text)

def greet_user(update, context):
    print('Вызван /start')
    update.message.reply_text('Hello! Commands: /start /guess')

def main():
    mybot = Updater(settings.API_KEY, use_context=True)
    dp = mybot.dispatcher
    dp.add_handler(CommandHandler('guess', guess_number))
    dp.add_handler(CommandHandler("start", greet_user))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))

    logging.info("Bot is start")
    
    mybot.start_polling()
    mybot.idle()

if __name__ == "__main__":
    main()
