import telebot
import firebase_admin
from firebase_admin import db
from telebot import types


cred = credentials.Certificate('rest.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://telebot-f26ac-default-rtdb.firebaseio.com"
})

# db = firebase_admin.db
ref = db.reference()
bot = telebot.TeleBot('1981321175:AAGfBt1LWcBrznwlfBC5mDLPAbBCbXoQlTc')


@bot.message_handler(commands=['start'])
def handle_start(message):
    user_markup = telebot.types.ReplyKeyboardMarkup(True)
    user_markup.row(('Записаться'))
    user_markup.row(('Свободное время'))
    bot.send_message(message.from_user.id,'Здравствуйте', reply_markup=user_markup)
    sent = bot.send_message(message.chat.id, 'Вы можете записаться онлайн. \n'
                                             'Выберите один из кнопок')
    bot.register_next_step_handler(sent, Subject)

@bot.message_handler(content_types=['text'])
def Subject(message):
    if message.text == 'Записаться':
        key = types.InlineKeyboardMarkup()
        bt = types.InlineKeyboardButton(text = '10:00', callback_data='10:00')
        bt1 = types.InlineKeyboardButton(text = '11:00', callback_data='11:00')
        bt2 = types.InlineKeyboardButton(text = '12:00', callback_data='12:00')
        bt3 = types.InlineKeyboardButton(text = '13:00', callback_data='13:00')
        bt4 = types.InlineKeyboardButton(text = '14:00', callback_data='14:00')
        bt5 = types.InlineKeyboardButton(text = '15:00', callback_data='15:00')
        bt6 = types.InlineKeyboardButton(text = '16:00', callback_data='16:00')
        bt7 = types.InlineKeyboardButton(text = '17:00', callback_data='17:00')
        bt8 = types.InlineKeyboardButton(text = '18:00', callback_data='18:00')
        bt9 = types.InlineKeyboardButton(text = '19:00', callback_data='19:00')
        key.add(bt, bt1, bt2, bt3, bt4, bt5, bt6, bt7, bt8, bt9)
        sent1 = bot.send_message(message.chat.id, 'Выберите свободное время', reply_markup=key)
        bot.register_next_step_handler(sent1, inlin)
@bot.callback_query_handler(func=lambda c: True)
def inlin(c):
    contains = db.child('zapis').child(c.data).get()
    cStr = ''+str(contains.val())
    if cStr == 'None':
        var = a == c.from_user.username
        user_ref = db.child('zapis'.child(c.data))

        user_ref.set({'name':'@'+a})
        bot.send_message(c.message.chat.id,'Спасибо. Вас записали')
    else:
        bot.send_message(c.message.chat.id,'******')
bot.polling(none_stop=True)



