from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, \
    InlineKeyboardButton, message
# config
from config import TOKEN, admins_ids
# Машина состояний
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
# Опросы v2.0
from typing import List
# from quizzer import Quiz
# bd
import sqlite3
from test import DBConnector

import asyncio
import json

bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
db_connector = DBConnector()


class inlineDataInput(StatesGroup):
    question = State()
    answer = State()


class DataInput(StatesGroup):
    webinar_time = State()


class PhoneDataInput(StatesGroup):
    kb = State()


class PostDataInput(StatesGroup):
    kb = State()


class PollDataInput(StatesGroup):
    kb = State()


async def is_admin_check(user_id):
    if user_id in admins_ids:
        return True
    return False


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.reply(f"Hi, {message.from_user.username}")
    # markup_request = ReplyKeyboardMarkup(resize_keyboard=True).add(
    # KeyboardButton('Отправить свой контакт ☎️', request_contact=True))
    markup = InlineKeyboardMarkup()
    url_book = InlineKeyboardButton('Kitap', url='https://www.google.com/')
    markup.add(url_book)
    await message.reply("китап сатып ал", reply_markup=markup)
    await message.reply("Отправьте ваш номер телефона:")
    await PhoneDataInput.kb.set()


@dp.message_handler(state=PhoneDataInput.kb)
async def put_Post(message: types.Message, state: FSMContext):
    nb_text = message.text
    db_connector.add_user(message.from_user.id, message.from_user.first_name, nb_text)
    await message.reply("Номер успешно сохранен!")
    await state.finish()


@dp.message_handler(commands=['commands'])
async def process_start_command(message: types.Message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    btn_1 = KeyboardButton('/start')
    btn_2 = KeyboardButton('/post')
    btn_3 = KeyboardButton('/poll')
    btn_4 = KeyboardButton('/getusers')
    btn_5 = KeyboardButton('/hour')
    btn_6 = KeyboardButton('/cancel')
    markup.add(btn_1, btn_2, btn_3, btn_4, btn_5, btn_6)
    await message.reply(
        "/start - start\n/post - юзерлерге жиберед\n/poll - опрос\n/getusers - барлык юзерлерди кору\n/hour - вебинар бастау",
        reply_markup=markup)


@dp.message_handler(commands=['post'], state=None)
async def echo_Post(message: types.Message):
    # list
    await message.reply("user-лерге не жибересиз:", reply=False)
    await PostDataInput.kb.set()


@dp.message_handler(state=PostDataInput.kb)
async def send_post(message, state: FSMContext):
    kb_text = message.text
    IDs = db_connector.get_all_users()

    for ID in IDs:
        await bot.send_message(ID[0], kb_text)

    await state.finish()


# Poll create script

@dp.message_handler(commands=['newpoll'])
async def new_poll(message: types.Message):
    await message.answer('Type question')
    await inlineDataInput.question.set()


@dp.message_handler(state=inlineDataInput.question)
async def get_question(mes: types.Message, state: FSMContext):
    pollid = db_connector.add_poll(mes.text)

    await state.update_data(pollid=pollid)

    await mes.answer('Type answers(one by one)')

    await inlineDataInput.answer.set()


@dp.message_handler(state=inlineDataInput.answer)
async def get_answer(mes: types.Message, state: FSMContext):
    data = await state.get_data()

    if mes.text.lower() != 'stop':
        pollanswerid = db_connector.add_pollanswer(data['pollid'], mes.text)
        await mes.answer("Write more answer or \"STOP\" for finish")

    else:
        await state.finish()

        poll = db_connector.get_poll(data['pollid'])

        poll_answers = db_connector.get_all_pollanswers_of_poll(data['pollid'])

        message = 'POLL!!!\nQuestion:\n    ' + poll[1]

        markup = InlineKeyboardMarkup()

        for poll_answer in poll_answers:
            btn = InlineKeyboardButton(poll_answer[2], callback_data="pa " + str(poll_answer[0]))
            markup.add(btn)

        await mes.answer(message, reply_markup=markup)


@dp.callback_query_handler(lambda call: call.data.startswith("pa"))
async def callback_pollanswer(call: types.CallbackQuery):
    await bot.answer_callback_query(call.id)

    pollanswer_id = int(call.data.split()[1])
    pollanswer = db_connector.get_pollanswer(pollanswer_id)

    db_connector.add_pollanswereduser(pollanswer_id, call.from_user.id, call.from_user.username)

    await bot.send_message(call.from_user.id, "Thanks!\nYour answer is " + pollanswer[2])


@dp.message_handler(commands=['all_polls'])
async def get_all_polls(mes: types.Message):
    polls = db_connector.get_all_polls()

    message_to_answer = "Polls: "

    counter = 1

    for poll in polls:
        message_to_answer += f"\n{counter}) /poll_{poll[0]}\n	{poll[1]}"
        counter += 1

    await mes.answer(message_to_answer)


@dp.message_handler(lambda mes: mes.text.startswith('/poll_'))
async def get_poll(mes: types.Message):
    poll_id = mes.text.split('_')[1]
    poll = db_connector.get_poll(poll_id)

    message_to_answer = f"Poll {poll_id}\nQuestion \"{poll[1]}\""

    poll_answers = db_connector.get_all_pollanswers_of_poll(poll_id)

    for poll_answer in poll_answers:
        poll_answer_users = db_connector.get_all_pollansweredusers_of_answer(poll_answer[0])
        message_to_answer += f"\nAnswer \"{poll_answer[2]}\"\n		Answer count: {len(poll_answer_users)}\n		Answered users list /pau_{poll_answer[0]}"

    await mes.answer(message_to_answer)


@dp.message_handler(lambda mes: mes.text.startswith("/pau_"))
async def get_poll_answer_users(mes: types.Message):
    poll_answer_id = int(mes.text.split('_')[1])

    users = db_connector.get_all_pollansweredusers_of_answer(poll_answer_id)

    message_to_answer = f"Answered users: "

    counter = 1

    for user in users:
        message_to_answer += f"\n{counter}){user[1]}-@{user[2]}"
        counter += 1

    await mes.answer(message_to_answer)


@dp.message_handler(commands=['poll'], state=None)
async def echo_Poll(message: types.Message):
    # list
    await message.reply("user-лерге не жибересиз:", reply=False)

    await PollDataInput.kb.set()


@dp.message_handler(content_types=['poll'], state=PollDataInput.kb)
async def send_poll(message: types.Message, state: FSMContext):
    msg_poll = await bot.send_poll(message.from_user.id,
                                   str(message.poll.question),
                                   [o.text for o in message.poll.options],
                                   is_anonymous=False)

    IDs = db_connector.get_all_users()

    for ID in IDs:
        if ID[0] != message.from_user.id:
            await bot.forward_message(ID[0], msg_poll.chat.id, msg_poll.message_id)

    await state.finish()


@dp.message_handler(commands=['getusers'])
async def get_users(message: types.Message):
    is_admin = await is_admin_check(message.from_user.id)

    if is_admin:

        users = db_connector.get_all_users()
        message_to_send = ''

        for user in users:
            message_to_send += f'Подписчик с именем {user[1]}:\n    ID: {user[0]}\n    Phone number: {user[2]}\n\n'

        await message.reply(message_to_send, reply=False)

    else:
        await message.reply('У вас нет прав на эту команду', reply=False)


GROUP_ID = '-426089346'


@dp.message_handler(commands=['poll'])
async def send_poll(message: types.Message):
    users = db_connector.get_all_users()
    for user in users:
        await bot.send_poll(user[0], question='question1', options=['op1', 'op2', 'op3'])


async def get_answer(update):
    answers = update.poll.options

    ret = ""

    for answer in answers:
        if answer.voter_count == 1:
            ret = answer.text
    return ret
    await bot.send_poll(chat_id=GROUP_ID, question=poll.question, options=poll.options, type="quiz",
                        correct_option_id=1, is_anonymous=True)


@dp.message_handler(commands=['hour'], state=None)
async def echo_hour(message: types.Message):
    await message.reply("канша сагаттан кейн вебинар:( тек кана сан жазу)", reply=False)
    await DataInput.webinar_time.set()


@dp.message_handler(state=DataInput.webinar_time)
async def put_Post(message: types.Message, state: FSMContext, ):
    message.text = float(message.text)
    webinar_time_text = message.text

    IDs = db_connector.get_all_users()

    for ID in IDs:
        for i in range(1, int(webinar_time_text) + 1):
            await bot.send_message(ID[0], f'вебинар {webinar_time_text} сагаттан кейн басталад.')
            webinar_time_text = int(webinar_time_text) - 1
            await asyncio.sleep(3)
        await bot.send_message(ID[0], "вебинар басталды")
    await state.finish()


# Хэндлер на текстовое сообщение с текстом “Отмена”
@dp.message_handler(commands=['cancel'])
async def cancel(message: types.Message):
    remove_keyboard = types.ReplyKeyboardRemove()
    await message.answer("Действие отменено.", reply_markup=remove_keyboard)


if __name__ == '__main__':
    executor.start_polling(dp)