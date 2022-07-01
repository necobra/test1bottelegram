import random

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from random import randint
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher.filters import Text

from bd import BotDB

bot = Bot(token='5502925067:AAGHrx-77qnydu_xcb9XE8vMaCVEpu4KKQA', parse_mode='html')
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

db = BotDB('database.db')


class Form(StatesGroup):
    ans = State()


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    rmk = types.reply_keyboard.ReplyKeyboardMarkup(resize_keyboard=True)
    b1 = types.reply_keyboard.KeyboardButton('Характеристика - имя')
    b2 = types.reply_keyboard.KeyboardButton('Портрет - имя')
    b3 = types.reply_keyboard.KeyboardButton('Інформація')
    rmk.row(b1, b2, b3)
    msg = "Меню"
    await bot.send_message(message.chat.id, msg, reply_markup=rmk)


@dp.message_handler(Text(startswith='Інформація'))
@dp.message_handler(commands=['info'])
async def info(message: types.Message):
    msg = "/add_pers\nname@\ndescrp@\nportrait(посилання або 0)@\ntopic(цифра))@\ntype(0-побічні чи 1-головні)@\n" \
          "(!після кожного @ - абзац)\n\n" \
          "/test_descrp a(0 чи 1-важність персонажів) b(номер теми, за замовчуванням-всі теми)\n" \
          "аналогічно /test_descrp_all, /test_photo\n\n" \
          "Список тем:\n" \
          "1 - різне\n" \
          "2 - 1 світова, революції\n" \
          "3 - встановлення ком режиму\n" \
          "4 - утв ком режиму\n" \
          "5 - зх тер міжвоєннтй період\n" \
          "6 - 2 св\n" \
          "7 - десталінізація\n" \
          "8 - загостр рад системи\n" \
          "9 - перебудова\n" \
          "10 - становлення незал України"
    await bot.send_message(message.chat.id, msg)


@dp.message_handler(commands=['test'])
async def test(message: types.Message):
    pass


async def important(st, photo):
    st += ' '
    z = st.find(' ')

    try:
        type = int(st[:z])
    except:
        type = 0

    try:
        topic = int(st[z + 1:])
    except:
        topic = 0

    if photo == 0:
        photo = -1
    elif photo == 1:
        photo = 0

    if type == 0:
        if topic == 0:
            rez = db.get_list_all(photo)
        else:
            rez = db.get_list_notype(topic, photo)
    elif topic == 0:
        rez = db.get_list_notopic(type, photo)
    else:
        rez = db.get_list(topic, type, photo)

    rez = rez.fetchall()
    return rez


@dp.message_handler(Text(startswith='Характеристика - имя'))
@dp.message_handler(commands=['test_descrp'])
async def test_descrp(message: types.Message, state: FSMContext):
    if message.text.startswith('Характеристика - имя'):
        st = message.text[21:]
    else:
        st = message.text[13:]

    rez = await important(st, 0)
    # print(rez)
    int1 = randint(0, len(rez) - 1)
    name = rez[int1][1]
    descrp = rez[int1][2]

    rmk = types.inline_keyboard.InlineKeyboardMarkup()
    b1 = types.inline_keyboard.InlineKeyboardButton(text="Відповідь", callback_data=f'name_ans={name}')
    rmk.add(b1)
    await bot.send_message(message.from_user.id, descrp, reply_markup=rmk)


@dp.message_handler(commands=['test_descrp_all'])
async def test_descrp_all(message: types.Message, state: FSMContext):
    if message.text.startswith('Характеристика - имя'):
        st = message.text[25:]
    else:
        st = message.text[17:]
    # print(st)
    rez = await important(st, 0)
    # print(rez)
    random.shuffle(rez)
    for i in rez:

        name = i[1]
        descrp = i[2]

        rmk = types.inline_keyboard.InlineKeyboardMarkup()
        b1 = types.inline_keyboard.InlineKeyboardButton(text="Відповідь", callback_data=f'name_ans={name}')
        rmk.add(b1)
        await bot.send_message(message.from_user.id, descrp, reply_markup=rmk)


@dp.callback_query_handler(Text(startswith='name_ans'))
async def test(callback: types.callback_query, state: FSMContext):
    name = callback.data[9:]
    text = f'{callback.message.text}\n\n<b>{name}</b>'
    await callback.message.edit_text(text)
    await callback.answer()


@dp.message_handler(Text(startswith='Портрет - имя'))
@dp.message_handler(commands=['test_photo'])
async def test_photo(message: types.Message, state: FSMContext):
    if message.text.startswith('Портрет - имя'):
        st = message.text[13:]
    else:
        st = message.text[11:]

    rez = await important(st, 1)
    # print(rez)
    int1 = randint(0, len(rez) - 1)
    name = rez[int1][1]
    url = rez[int1][3]

    rmk = types.inline_keyboard.InlineKeyboardMarkup()
    b1 = types.inline_keyboard.InlineKeyboardButton(text="Відповідь", callback_data=f'name_ans={name}')
    rmk.add(b1)
    await bot.send_message(message.from_user.id, url, reply_markup=rmk)


@dp.message_handler(commands=['add_pers'])
async def add_pers(message: types.Message):
    text = message.text
    ass = text.split('\n')
    # print(ass)
    name = ass[1]
    descrp = ass[2]
    portrait = ass[3]
    topic = ass[4]
    type = ass[5]
    db.add_reminder(name, descrp, portrait, topic, type)
    await bot.send_message(message.from_user.id, "+")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
