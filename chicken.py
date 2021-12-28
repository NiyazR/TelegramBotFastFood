import telebot
from telebot import types
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate('rest.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://botrestaurant-db316-default-rtdb.firebaseio.com"
})

# db = firebase_admin.db
ref = db.reference()

bot = telebot.TeleBot('5070160258:AAHQWx3JuCrPpQw6-klbOSYsOkuhqRbbyII')


@bot.message_handler(commands=['start'])
def start(message):
    start_menu = types.ReplyKeyboardMarkup(True, True)
    start_menu.row('🔥 Chicken hit', '🥳 Shares')
    start_menu.row('🍱 Menu', '🍟 Sets')
    start_menu.row('🕒 Delivery', '📞 Contacts')
    start_menu.row('📍Address', '📝Review')
    bot.send_message(message.chat.id, "Welcome to Adal Chicken Bot"
                                      "\nTaraz Chicken🍖🔥😎 : "
                                      "\n- 🍗 The taste you were looking for;"
                                      "\n- 🕌 Halal Product;"
                                      "\n- 🕒 11:00-00:00 (seven days a week);"
                                      "\n- 📲 +77071887071;"
                                      "\n"
                                      "\nDelivery / Self-call; "
                                      "\nWe work seven days a weekх", reply_markup=start_menu)


def back(message):
    start_menu = types.ReplyKeyboardMarkup(True, True)
    start_menu.row('🔥 Chicken hit', '🥳 Shares')
    start_menu.row('🍱 Menu', '🍟 Sets')
    start_menu.row('🕒 Delivery', '📞 Contacts')
    start_menu.row('📍Address', '📝Review')
    bot.send_message(message.chat.id, "Main menu", reply_markup=start_menu)


@bot.message_handler(content_types=['text'])
def handle_text(message):
    chat_id = message.chat.id
    photo = 'https://b.zmtcdn.com/data/menus/182/6113182/67df8122e19d5af412863528bf81cddc.jpg'

    photo13 = 'https://ltdfoto.ru/images/Screenshot_3fd7a9410844ae7f1.png'
    photo10 = 'https://ltdfoto.ru/images/Screenshot_48cd380ae66b251f1.png'
    photo11 = 'https://ltdfoto.ru/images/Screenshot_5f546fc354ffdc40d.png'
    photo12 = 'https://ltdfoto.ru/images/Screenshot_6cd27a2006aaf2860.png'
    photo14 = 'https://ltdfoto.ru/images/Screenshot_48cd380ae66b251f1.png'

    photo5 = 'https://ltdfoto.ru/images/Screenshot_19cefd2837c8f6425.png'
    photo6 = 'https://ltdfoto.ru/images/Screenshot_245b7df162d45042a.png'

    file = photo13, photo10, photo11, photo12, photo14, photo5, photo6, photo

    if message.text == '🔥 Chicken hit':
        second_menu = types.ReplyKeyboardMarkup(True, True)
        second_menu.row('Shin', 'Wings', 'Strips', 'Chicken legs', 'Bytes')
        second_menu.row('Back')

        second_menu.row('2')

        bot.send_message(message.chat.id, "Chicken", reply_markup=second_menu)

    elif message.text == '2':
        second_menu = types.ReplyKeyboardMarkup(True, True)
        second_menu.row('Cola', 'Sprite', 'Ayran', 'Juice', 'Enegetic')
        second_menu.row('1')
        second_menu.row('3')

        bot.send_message(message.chat.id, "Chicken", reply_markup=second_menu)

    elif message.text == '3':
        second_menu = types.ReplyKeyboardMarkup(True, True)
        second_menu.row('fries mini', 'fries standard', 'fries medium', 'fries mega', 'fries max')
        second_menu.row('2')
        second_menu.row('4')

        bot.send_message(message.chat.id, "Chicken", reply_markup=second_menu)

    elif message.text == '4':
        second_menu = types.ReplyKeyboardMarkup(True, True)
        second_menu.row('Mini Basket Chicken', 'Medium Basket Chicken', 'Max Basket Chicken')
        second_menu.row('3')
        second_menu.row('5')
        second_menu.row('Back')

        bot.send_message(message.chat.id, "Chicken", reply_markup=second_menu)





    elif message.text == '🕒 Delivery':

        markup = types.ReplyKeyboardMarkup()

        sent = bot.send_message(message.chat.id, "Write your suitable time for delivery", reply_markup=markup)
        bot.register_next_step_handler(sent, inlin)

    elif message.text == '🍱 Menu':
        bot.send_media_group(message.chat.id, [types.InputMediaPhoto(photo)])

    elif message.text == '🍟 Sets':
        bot.send_media_group(message.chat.id, [types.InputMediaPhoto(photo10)])
        bot.send_media_group(message.chat.id, [types.InputMediaPhoto(photo11)])
        bot.send_media_group(message.chat.id, [types.InputMediaPhoto(photo12)])
        bot.send_media_group(message.chat.id, [types.InputMediaPhoto(photo13)])
        bot.send_media_group(message.chat.id, [types.InputMediaPhoto(photo14)])



    elif message.text == '📍Address':
        bot.send_message(message.chat.id, "Kazakhstan, Taraz, st. Aiteke bi, 3A")


    elif message.text == '📞 Contacts':
        bot.send_message(message.chat.id, "+77071887071")

    elif message.text == '🥳 Shares':
        bot.send_media_group(message.chat.id, [types.InputMediaPhoto(photo6)])
        bot.send_media_group(message.chat.id, [types.InputMediaPhoto(photo5)])

    elif message.text == '📝Review':
        markup = types.ReplyKeyboardMarkup()

        sent = bot.send_message(message.chat.id, "Write your review...", reply_markup=markup)
        bot.register_next_step_handler(sent, review)



    elif message.text == 'Back':

        back(message)

    # Еда
    if message.text == 'Shin':
        bot.send_message(message.from_user.id,
                         'Your delivery will be delivered in 45 minutes. Expect! Good appetite!😋')
        user = message.text
        print(user)
        contains = ref.child('Регистрация заказов').child('mealtort').get()
        cStr = "" + str(contains)

        user_ref = ref.child('Регистрация заказов').child('mealtort')
        user_ref.set(user)
        bot.reply_to(message, "Thank you for choosing us☺")


    elif message.text == 'Wings':
        bot.send_message(message.from_user.id,
                         'Your delivery will be delivered in 45 minutes. Expect! Good appetite!😋')
        user = message.text
        print(user)
        contains = ref.child('Регистрация заказов').child('mealush').get()
        cStr = "" + str(contains)

        user_ref = ref.child('Регистрация заказов').child('mealush')
        user_ref.set(user)
        bot.reply_to(message, "Thank you for choosing us☺")
    elif message.text == 'Chicken legs':
        bot.send_message(message.from_user.id,
                         'Your delivery will be delivered in 45 minutes. Expect! Good appetite!😋')
        user = message.text
        print(user)
        contains = ref.child('Регистрация заказов').child('mealtwo').get()
        cStr = "" + str(contains)

        user_ref = ref.child('Регистрация заказов').child('mealtwo')
        user_ref.set(user)
        bot.reply_to(message, "Thank you for choosing us☺")
    elif message.text == 'Strips':
        bot.send_message(message.from_user.id,
                         'Your delivery will be delivered in 45 minutes. Expect! Good appetite!😋')
        user = message.text
        print(user)
        contains = ref.child('Регистрация заказов').child('mealone').get()
        cStr = "" + str(contains)

        user_ref = ref.child('Регистрация заказов').child('mealone')
        user_ref.set(user)
        bot.reply_to(message, "Thank you for choosing us☺")
    elif message.text == 'Bytes':
        bot.send_message(message.from_user.id,
                         'Your delivery will be delivered in 45 minutes. Expect! Good appetite!😋')
        user = message.text
        print(user)
        contains = ref.child('Регистрация заказов').child('meal').get()
        cStr = "" + str(contains)

        user_ref = ref.child('Регистрация заказов').child('meal')
        user_ref.set(user)
        bot.reply_to(message, "Thank you for choosing us☺")


@bot.message_handler(content_types=['text'])
def inlin(message):
    if message == "None":
        bot.send_message(message.chat.id, "Try to write...")

    else:
        bot.reply_to(message, "Thanks. You're in our database")
        userr = message.from_user.username
        user1 = message.text
        ref.child('Registration').child('Time').push(user1)
        ref.push({'name': '@' + userr})


@bot.message_handler(content_types=['text'])
def review(message):
    if message == "None":
        bot.send_message(message.chat.id, "Try to write...")
    else:
        bot.reply_to(message, "Thanks for your feedback")
        userr = message.from_user.username
        print(userr)
        user1 = message.text
        print(user1)
        ref.child('Review').child('Clientone').push(user1)
        ref.push({'name':'@'+userr})


bot.polling(none_stop=True)
