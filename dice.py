from random import randint

def dice_number(update, context):
    if context.args:
        try: 
            user_number = int(context.args[0])
            bet = int(context.args[1])
            gain=context.user_data['gain']
            message = play_dice(user_number, bet, gain, context)
        except (TypeError, ValueError):
            message = 'Enter an integer'
        except (KeyError):
            message = 'Your gain is 0. Please use /gain'  
    else:
        message = '\nEnter an integer \nUse /dice #number# #bet#'
    update.message.reply_text(message)

def play_dice(user_number, bet, gain, context):
    if user_number<2 or user_number>12:
        message = 'Number out of range. \nPlease enter a number from 2 to 12' 
    elif bet<1 or bet>gain:
        message = f'Bet is not allowed. Your gain is {gain}'
    else:
        score1 = randint(1,6)
        score2 = randint(1,6)
        total_score = score1 + score2
        if total_score==user_number:
            gain += 4 * bet
            message = f"На первом кубике выпало {score1}. На втором кубике выпало {score2}. \nВы выйграли : {bet}х4, ваш счет {gain}"
            context.user_data["gain"] = gain
        elif total_score < 7 and user_number<7:
            gain += bet
            message = f"На первом кубике выпало {score1}. На втором кубике выпало {score2}. \nВы выйграли : {bet}, ваш счет {gain}"
            context.user_data["gain"] = gain
        elif total_score > 7 and user_number>7:
            gain += bet
            message = f"На первом кубике выпало {score1}. На втором кубике выпало {score2}. \nВы выйграли : {bet}, ваш счет {gain}"
            context.user_data["gain"] = gain
        else:
            gain-= bet
            message = f"На первом кубике выпало {score1}. На втором кубике выпало {score2}. \nСтавка проиграна, ваш счет {gain}"
            context.user_data["gain"] = gain
    return message

def show_rules(update, context):
    pic_filename='telegrammbot\img\game_dice.png'
    chat_id = update.effective_chat.id
    context.bot.send_photo(chat_id=chat_id, photo=open(pic_filename, 'rb'))

def get_gain(update, context):
    context.user_data["gain"] = 100
    update.message.reply_text(f"Your gain is {context.user_data['gain']}!")