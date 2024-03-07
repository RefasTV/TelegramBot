##### Libriaries #####
import telebot
from telebot import types
import db


##### Variables #####
database = db.DBBot('dataBase.db')
bot = telebot.TeleBot("6591485398:AAH-zBRlqzfEO3ySR4N5rHewzKh6IWuwefQ", parse_mode=None)
newAdd = []


##### Create a markup with all buttons #####
def get_markup():
    markup = types.ReplyKeyboardMarkup(row_width=2)
    newBuy = types.KeyboardButton("Добавить новую покупку!")
    history = types.KeyboardButton("История покупок!")
    statistic = types.KeyboardButton("Статистика!")
    markup.row(newBuy, history, statistic)

    return markup


# if command /start is written! #
@bot.message_handler(commands=['start'])
def start(message):
    if database.user_exists(message.from_user.id) == False:
        database.add_user(message.from_user.id)

    markup = get_markup()

    try:
        bot.send_message(message.from_user.id, "Привет, " + message.from_user.first_name + " " + message.from_user.last_name + ". Я твой бот по расходам! \nПока что я умею только добавлять тебя в базу клиентов, добавлять покупки и выводить их историю, но скоро научусь чему-нибудь еще!", reply_markup=markup)
    except:
        bot.send_message(message.from_user.id, "Привет, Таинсвенный незнакомец! Я твой бот по расходам! \nПока что я умею только добавлять тебя в базу клиентов, добавлять покупки и выводить их историю, но скоро научусь чему-нибудь еще!", reply_markup=markup)

# if something is written! #
@bot.message_handler(content_types=['text'])
def message_analize(message):

    ##### Insert a new buy #####
    if message.text == "Добавить новую покупку!":
        insert_new_buy(message)

    ##### Statistics #####
    elif message.text == "Статистика!":
        markup = types.ReplyKeyboardMarkup(row_width=2)
        categ = types.KeyboardButton("По категории")
        place = types.KeyboardButton("По месту")
        date = types.KeyboardButton("По дате (пока не работает)")
        markup.row(categ, place, date)

        msg = bot.send_message(message.chat.id, "Расходы по какому критерию ты хочешь увидеть?", reply_markup=markup)
        bot.register_next_step_handler(msg, statistic)
        



    ##### History #####
    elif message.text == "История покупок!":
        records = database.get_records(message.from_user.id)

        if len(records):
            bot.send_message(message.chat.id, "Найденные записи:")
            print(records)
            for r in records:
                print(r)
                bot.send_message(message.chat.id, "Потрачено: " + str(r[2]) + "\nКатегория: " + str(r[3]) + "\nМесто: " + str(r[4]) + "\nДата: " + str(r[5]))
        else:
            bot.send_message(message.chat.id, "Записей не обнаружено!")
        
        bot.send_message(message.chat.id, "Могу ли я еще как-то помочь?", reply_markup=get_markup())

    else:
        markup = get_markup()
        bot.send_message(message.chat.id, "Прости, но я не знаю что ты хочешь. Возможно что-то из этих кнопок подойдет <3", reply_markup=markup)




'''
#######################            BOT FUNCTIONS              ################################
'''

##### Insert new buy #####
def insert_new_buy(message):
    msg = bot.send_message(message.chat.id, "Введите сумму: ")
    bot.register_next_step_handler(msg, insert_money)
    
##### Insert money for new buy #####
def insert_money(message):
    if len(newAdd) == 0:
        money = message.text

        try:
            money = int(money)
        except:
            msg = bot.send_message(message.chat.id, 'ДЕНЬГИ НЕ ИЗМЕРЯЮТСЯ В СТРОКАХ. ОНИ ЧИСЛА!\nНапиши что-нибудь если ты понял <3')
            bot.register_next_step_handler(msg, insert_new_buy)
            return
        
        newAdd.append(money)
    

    ################## id:s for category insert ###########################
    msg = bot.send_message(message.chat.id, "Введите категорию: ")

    cat = database.get_categories(message.from_user.id)
    
    for i in range(len(cat)):
        bot.send_message(message.chat.id,  str(i) + ": " + cat[i][0])
    bot.send_message(message.chat.id, "-1: другое")


    msg = bot.send_message(message.chat.id, "Введите id категории: ")
    bot.register_next_step_handler(msg, insert_category)


##### Insert category for new buy #####
def insert_category(message):
    cat = database.get_categories(message.from_user.id)
    try:
        index = int(message.text)
        if index != -1:
            newAdd.append(cat[index][0])

            msg = bot.send_message(message.chat.id, "Введите место: ")
            place = database.get_places(message.from_user.id)
        
            for i in range(len(place)):
                bot.send_message(message.chat.id,  str(i) + ": " + place[i][0])
            bot.send_message(message.chat.id, "-1: другое")


            msg = bot.send_message(message.chat.id, "Введите id места: ")
            bot.register_next_step_handler(msg, insert_place)

        else:
            msg = bot.send_message(message.chat.id, "Введите название новой категории: ")
            bot.register_next_step_handler(msg, insert_new_category)
    except:
        msg = bot.send_message(message.chat.id, "Хватит ломать мой код! Напиши что-нибудь если ты больше так не будешь <3 !")
        bot.register_next_step_handler(msg, insert_money)

def insert_new_category(message):
    if len(newAdd) < 2:
        newAdd.append(message.text)

    msg = bot.send_message(message.chat.id, "Введите место: ")

    place = database.get_places(message.from_user.id)
    
    for i in range(len(place)):
        bot.send_message(message.chat.id,  str(i) + ": " + place[i][0])
    bot.send_message(message.chat.id, "-1: другое")


    msg = bot.send_message(message.chat.id, "Введите id места: ")
    bot.register_next_step_handler(msg, insert_place)



##### Insert place for new buy #####
def insert_place(message):
    place = database.get_places(message.from_user.id)
    try:
        index = int(message.text)
        if index != -1:
            newAdd.append(place[index][0])

            msg = bot.send_message(message.chat.id, "Введите дату: ")
            bot.register_next_step_handler(msg, insert_date)
        else:
            msg = bot.send_message(message.chat.id, "Введите название нового места: ")
            bot.register_next_step_handler(msg, insert_place_by_text)
    except:
        msg = bot.send_message(message.chat.id, "Хватит ломать мой код! Напиши что-нибудь если ты больше так не будешь <3 !")
        bot.register_next_step_handler(msg, insert_new_category)

def insert_place_by_text(message):
    newAdd.append(message.text)
    msg = bot.send_message(message.chat.id, "Введите дату: ")
    bot.register_next_step_handler(msg, insert_date)








##### Insert date for new buy #####
def insert_date(message):
    global newAdd
    date = message.text
    newAdd.append(date)
    print(newAdd)

    database.add_record(message.from_user.id, newAdd[0], 
                        newAdd[2], newAdd[1])
    newAdd = []
    bot.send_message(message.chat.id, "Все отлично, операция прошла успешно!")

    bot.send_message(message.chat.id, "Могу ли я еще как-то помочь?", reply_markup=get_markup())



##### Statistic #####
def statistic(message):
    if message.text == "По категории":
        cat = database.get_categories(message.from_user.id)
    
        for i in range(len(cat)):
            bot.send_message(message.chat.id,  str(i) + ": " + cat[i][0])
        
        msg = bot.send_message(message.chat.id, "Введите id категории: ")
        bot.register_next_step_handler(msg, get_stats_by_category)
        

    elif message.text == "По месту":
        cat = database.get_places(message.from_user.id)
    
        for i in range(len(cat)):
            bot.send_message(message.chat.id,  str(i) + ": " + cat[i][0])
        
        msg = bot.send_message(message.chat.id, "Введите id места: ")
        bot.register_next_step_handler(msg, get_stats_by_places)
        

    elif message.text == "По дате":
        pass

    else:
        bot.send_message(message.chat.id, "Простите, но я не знаю такой команды. Возможно что-то из этого поможет <3", reply_markup=get_markup())



##### Get stats by category #####
def get_stats_by_category(message):
    cat = database.get_categories(message.from_user.id)
    try:
        msg = int(message.text)
        records = database.get_records_by_categories(cat[msg][0], message.from_user.id)

        if len(records):
            bot.send_message(message.chat.id, "Найденные записи:")
            for r in records:
                bot.send_message(message.chat.id, "Потрачено: " + str(r[2]) + "\nКатегория: " + str(r[3]) + "\nМесто: " + str(r[4]) + "\nДата: " + str(r[5]))

        else:
            bot.send_message(message.chat.id, "Записей не обнаружено!")
        
        bot.send_message(message.chat.id, "Могу ли я еще как-то помочь?", reply_markup=get_markup())
    except:
        bot.send_message(message.chat.id, "Произошла ошибка. Напишите что-нибудь чтобы начать снова.")
        return



##### Get stats by place #####
def get_stats_by_places(message):
    cat = database.get_places(message.from_user.id)
    try:
        msg = int(message.text)
        records = database.get_records_by_places(cat[msg][0], message.from_user.id)

        if len(records):
            bot.send_message(message.chat.id, "Найденные записи:")
            for r in records:
                bot.send_message(message.chat.id, "Потрачено: " + str(r[2]) + "\nКатегория: " + str(r[3]) + "\nМесто: " + str(r[4]) + "\nДата: " + str(r[5]))

        else:
            bot.send_message(message.chat.id, "Записей не обнаружено!")
        
        bot.send_message(message.chat.id, "Могу ли я еще как-то помочь?", reply_markup=get_markup())
    except:
        msg = bot.send_message(message.chat.id, "Произошла ошибка. Напишите что-нибудь чтобы начать снова.")
        return


bot.polling(none_stop=True)