from telegram.ext import Updater
def main():
    mybot = Updater("809111474:AAENYVUwhxOMNKTOm5zkEjoKRhj9smt2NZk", use_context=True)
    mybot.start_polling()
    mybot.idle()
main()