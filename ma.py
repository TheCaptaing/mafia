from telebot import TeleBot
from time import sleep
import db

API_KEY='6581397403:AAEZKO9-2ZpNR0E6mnQjusWfbt15GOD3tJU'
bot = TeleBot(API_KEY)
game = False
night = False
result = '.'
first = 0
def get_killed(night):
    if not night:
        username_killed=db.citizen_kill()
        return f'Горожани выгнали: {username_killed}'
    else:
        username_killed=db.mafia_kill()
        return f'Мафия убила: {username_killed}'

def game_loop(message):
    global night,game,result, first
    while game:
        msg = get_killed(night)
        if msg !='Мафия убила: никого' and result=='.' and night==True:
            bot.send_message(message.chat.id,f'мафия сделала выбор, очередь за доктором')
            sleep(20)
            bot.send_message(message.chat.id,msg)
            bot.send_message(message.chat.id,result)
        elif first!=0:
            bot.send_message(message.chat.id,f'{msg}')


        sleep(5)
        winner = db.check_winner()
        if winner == 'maf' or winner == 'cit':
            game=False
            bot.send_message(message.chat.id,f'конец. победа за:{winner}')
            return
        if not night:
            bot.send_message(message.chat.id,'Наступает ночь')
            sleep(5)
        else:
            bot.send_message(message.chat.id,'Наступает утро')
            sleep(5)
        db.clear(dead=False)
        night=not night
        alive = db.get_alive()
        alive='\n'.join(alive)
        bot.send_message(message.chat.id, f'В игре:\n{alive}')
        first=1
        sleep(30)


# @bot.message_handler(commands=['start'])
# def start(message):
#     bot.send_message(message.chat.id, text=f'Если хоч играть пиши "готов играть" мне в лс')

@bot.message_handler(func=lambda m: m.text.lower() == 'готов играть' and m.chat.type=='private')
def send_text(message):
    bot.send_message(message.chat.id, text=f'{message.from_user.first_name} играет')
    bot.send_message(message.from_user.id, text='Вы добавлены')
    db.insert_player(player_id=message.from_user.id, username=message.from_user.first_name)


@bot.message_handler(commands=['game'])
def gamee(message):
    if message.chat.type in ('group', 'supergroup'):
        global game
        players=db.players_amount()
        if players >=5 and not game:
            db.set_roles(players)
            roles =db.get_playeridrole() 
            # mafianames = db.get_mafia()
            # for player_id, role in roles:
            #     bot.send_message(player_id,text=role)
            #     if role=='mafia':
            #         bot.send_message(player_id, text=f'Вся мафия: \n{mafianames}')
            game = True
            bot.send_message(message.chat.id, text='Игра началась')
            db.clear(dead=True)
            game_loop(message)
            return
        bot.send_message(message.chat.id, text=f'Минимум 5 игроков!')
    else:
        bot.send_message(message.chat.id, text=f'Пиши в группу!')

@bot.message_handler(commands=['kick'])
def kick(message):
    if message.chat.type in ('group', 'supergroup'):
        username = ' '.join(message.text.split(" ")[1:])
        usernames = db.get_alive()
        if not night:
            if not username in usernames:
                bot.send_message(message.chat.id, text=f'Нет такого')
                return
            voted = db.vote('citizen_vote',username,message.from_user.id)
            if voted:
                bot.send_message(message.chat.id, text=f'Ваш голос учитан')
                return
            bot.send_message(message.chat.id, text=f'Вы уже голосовали')
            return
        else:
            bot.send_message(message.chat.id, text=f'Щас ночь, низя кикать')
    else:
        bot.send_message(message.chat.id, text=f'Пиши в группу!')

@bot.message_handler(commands=['kill'])
def kill(message):
    if message.chat.type=='private':
        username = ' '.join(message.text.split(" ")[1:])
        usernames = db.get_alive()
        mafias= db.get_mafia()
        if night:
            if username in usernames:
                if not message.from_user.first_name in mafias:
                    bot.send_message(message.from_user.id, text=f'Вы не мафия')
                    return
                voted = db.vote('mafia_vote',username,message.from_user.id)
                if voted:
                    bot.send_message(message.from_user.id, text=f'Ваш голос учитан')
                    return
                bot.send_message(message.from_user.id, text=f'Вы уже голосовали')
                return
            else:
                bot.send_message(message.from_user.id, text=f'Таких нет')
        else:
            bot.send_message(message.from_user.id, text=f'Щас не ночь(нельзя убивать)')
    else:
        bot.send_message(message.chat.id, text=f'Пиши мне в личку!')

@bot.message_handler(commands=['check'])
def check(message):
    bot.send_message(message.chat.id, text=db.check_winner())
        
@bot.message_handler(commands=['players'])
def check(message):
    names = db.get_name()
    names = '\n'.join(names)
    bot.send_message(message.chat.id, text=f'В списке: \n{names}')
        

        
@bot.message_handler(commands=['heal'])
def heal(message):
    global result
    if message.chat.type=='private':
        if db.get_doctor()== message.from_user.first_name:
            username = ' '.join(message.text.split(" ")[1:])
            dead = db.get_dead()
            if night:
                try1=1
                if not username in dead:
                    bot.send_message(message.from_user.id, text=f'Он был жив')
                    d_voted_mimo = db.d_voted_mimo(message.from_user.id)
                    result = 'Доктор приехал не по адресу'
                    return 
                d_voted = db.heal(username,message.from_user.id)
                if not d_voted:
                    bot.send_message(message.from_user.id, f'Вы воскресили:\n{username}')
                    result= 'Доктор приехал по адресу'
                    return
                bot.send_message(message.from_user.id, text=f'Вы уже лечили')
                return
            else:
                bot.send_message(message.from_user.id, text=f'Щас не ночь(нельзя лечить)')
        else:
            bot.send_message(message.from_user.id, text=f'not a doc!')
            
    else:
        bot.send_message(message.from_user.id, text=f'Пиши мне в личку!')

if __name__ == '__main__':
    bot.polling(none_stop=True)
#bot.infinity_polling() 
