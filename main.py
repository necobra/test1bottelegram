import random

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from aiogram import Bot, Dispatcher, executor, types
from random import randint
from aiogram.dispatcher.filters import Text

from db import BotDB

bot = Bot(token='5502925067:AAGHrx-77qnydu_xcb9XE8vMaCVEpu4KKQA', parse_mode='html')
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

db = BotDB('database.db')


class Form(StatesGroup):
    subject_id = State()
    history = State()
    math = State()
    eng = State()
    topics = State()
    topic = State()
    new_topic = State()
    change = State()
    change_own = State()
    add_q = State()
    cin_new_q = State()
    edit_q = State()
    edit_q_q = State()
    edit_q_ans = State()


@dp.message_handler(commands=['test'], state="*")
async def test(message: types.Message, state: FSMContext):
    print(await state.get_state())


@dp.message_handler(Text(startswith='Вибрати інший предмет'), state="*")
@dp.message_handler(commands=['start'], state="*")
@dp.message_handler(commands=['start'], state=None)
async def start(message: types.Message, state: FSMContext):
    await state.finish()

    rmk = types.reply_keyboard.ReplyKeyboardMarkup(resize_keyboard=True)
    b1 = types.reply_keyboard.KeyboardButton('Історія ЗНО')
    b2 = types.reply_keyboard.KeyboardButton('Математика')
    b3 = types.reply_keyboard.KeyboardButton('Англ(тест)')
    rmk.row(b1, b2, b3)
    msg = "Виберіть потрібний предмет"
    await bot.send_message(message.chat.id, msg, reply_markup=rmk)


@dp.message_handler(Text(startswith='Історія ЗНО'), state=Form.history)
@dp.message_handler(Text(startswith='Історія ЗНО'), state=None)
async def history(message: types.Message, state: FSMContext):
    await Form.history.set()
    async with state.proxy() as qdata:
        qdata['subject_id'] = 1

    rmk = types.reply_keyboard.ReplyKeyboardMarkup(resize_keyboard=True)
    b0 = types.reply_keyboard.KeyboardButton('Вибрати інший предмет')
    b1 = types.reply_keyboard.KeyboardButton('Тема')
    b2 = types.reply_keyboard.KeyboardButton('Редагування')

    rmk.row(b1, b2, b0)
    msg = "Меню історії"
    await bot.send_message(message.chat.id, msg, reply_markup=rmk)


@dp.message_handler(Text(startswith='Вибрати інший предмет'), state="*")
async def func(message: types.Message, state: FSMContext):
    await start(message, state)


@dp.message_handler(Text(startswith='Редагування'), state=Form.history)
async def func(message: types.Message, state: FSMContext):
    await Form.change.set()
    rmk = types.reply_keyboard.ReplyKeyboardMarkup(resize_keyboard=True)
    b0 = types.reply_keyboard.KeyboardButton('Повернутися назад')
    b1 = types.reply_keyboard.KeyboardButton('Редагувати пріоритети тем')
    b2 = types.reply_keyboard.KeyboardButton('Редагувати назви тем')

    rmk.row(b1, b2, b0)
    msg = "Пам'ятай, в тебе завжди є вибір(напевно)"
    await bot.send_message(message.chat.id, msg, reply_markup=rmk)


@dp.message_handler(Text(startswith='Повернутися назад'), state=Form.change)
async def func(message: types.Message, state: FSMContext):
    await history(message, state)


@dp.message_handler(Text(startswith='Редагувати пріоритети тем'), state=Form.change)
async def func(message: types.Message, state: FSMContext):
    async with state.proxy() as qdata:
        subject_id = qdata['subject_id']
    topics_list = db.get_topics(subject_id)
    topics_list.sort(key=lambda x: x[3])
    # print(topics_list)
    for topic in topics_list:
        msg = f'{topic[1]}\n{topic[3]}'
        rmk = types.inline_keyboard.InlineKeyboardMarkup()
        b1 = types.inline_keyboard.InlineKeyboardButton(text="+1", callback_data=f'change_priot?{topic[0]}?+1')
        b2 = types.inline_keyboard.InlineKeyboardButton(text="-1", callback_data=f'change_priot?{topic[0]}?-1')
        b3 = types.inline_keyboard.InlineKeyboardButton(text="Поміняти на обране число",
                                                        callback_data=f'change_priot?{topic[0]}?=')
        rmk.row(b1, b2, b3)
        await bot.send_message(message.from_user.id, msg, reply_markup=rmk)


@dp.callback_query_handler(Text(startswith='change_priot'), state=Form.change)
async def func(callback: types.callback_query, state: FSMContext):
    data = callback.data.split('?')
    topic_id = int(data[1])
    act = data[2]
    # get priot
    priot = int(callback.message.text.split('\n')[1])
    # print(priot)
    if act == '+1':
        db.update_topic_priot(topic_id, priot + 1)
        text = callback.message.text.split('\n')[0] + f"\n{priot + 1}"

        rmk = types.inline_keyboard.InlineKeyboardMarkup()
        b1 = types.inline_keyboard.InlineKeyboardButton(text="+1", callback_data=f'change_priot?{topic_id}?+1')
        b2 = types.inline_keyboard.InlineKeyboardButton(text="-1", callback_data=f'change_priot?{topic_id}?-1')
        b3 = types.inline_keyboard.InlineKeyboardButton(text="Поміняти на обране число",
                                                        callback_data=f'change_priot?{topic_id}?=')
        rmk.row(b1, b2, b3)
        await callback.message.edit_text(text, reply_markup=rmk)
    elif act == '-1':
        db.update_topic_priot(topic_id, priot - 1)
        text = callback.message.text.split('\n')[0] + f"\n{priot - 1}"

        rmk = types.inline_keyboard.InlineKeyboardMarkup()
        b1 = types.inline_keyboard.InlineKeyboardButton(text="+1", callback_data=f'change_priot?{topic_id}?+1')
        b2 = types.inline_keyboard.InlineKeyboardButton(text="-1", callback_data=f'change_priot?{topic_id}?-1')
        b3 = types.inline_keyboard.InlineKeyboardButton(text="Поміняти на обране число",
                                                        callback_data=f'change_priot?{topic_id}?=')
        rmk.row(b1, b2, b3)
        await callback.message.edit_text(text, reply_markup=rmk)
    else:
        async with state.proxy() as qdata:
            qdata['topic_id'] = topic_id
            qdata['message'] = callback.message

        await Form.change_own.set()
        rmk = types.reply_keyboard.ReplyKeyboardMarkup(resize_keyboard=True)
        b = types.reply_keyboard.KeyboardButton('Відміна')
        rmk.add(b)
        msg = "Введіть число:"
        # print(callback.message)
        await bot.send_message(callback.message.chat.id, msg, reply_markup=rmk)


@dp.message_handler(Text(startswith='Відміна'), state=Form.change_own)
async def func(message: types.Message, state: FSMContext):
    await Form.change.set()
    rmk = types.reply_keyboard.ReplyKeyboardMarkup(resize_keyboard=True)
    b0 = types.reply_keyboard.KeyboardButton('Повернутися назад')
    b1 = types.reply_keyboard.KeyboardButton('Редагувати пріоритети тем')
    b2 = types.reply_keyboard.KeyboardButton('Редагувати назви тем')

    rmk.row(b1, b2, b0)
    msg = "Ок"
    await bot.send_message(message.chat.id, msg, reply_markup=rmk)


@dp.message_handler(state=Form.change_own)
async def func(message: types.Message, state: FSMContext):
    try:
        num = int(message.text)
        async with state.proxy() as qdata:
            topic_id = qdata['topic_id']
            qmessage = qdata['message']
        db.update_topic_priot(topic_id, num)
        msg = "👌"
        text = qmessage.text.split('\n')[0] + f"\n{num}"

        rmk = types.inline_keyboard.InlineKeyboardMarkup()
        b1 = types.inline_keyboard.InlineKeyboardButton(text="+1", callback_data=f'change_priot?{topic_id}?+1')
        b2 = types.inline_keyboard.InlineKeyboardButton(text="-1", callback_data=f'change_priot?{topic_id}?-1')
        b3 = types.inline_keyboard.InlineKeyboardButton(text="Поміняти на обране число",
                                                        callback_data=f'change_priot?{topic_id}?=')
        rmk.row(b1, b2, b3)
        await qmessage.edit_text(text, reply_markup=rmk)
    except:
        msg = "Упс"
    await Form.change.set()
    rmk = types.reply_keyboard.ReplyKeyboardMarkup(resize_keyboard=True)
    b0 = types.reply_keyboard.KeyboardButton('Повернутися назад')
    b1 = types.reply_keyboard.KeyboardButton('Редагувати пріоритети тем')
    b2 = types.reply_keyboard.KeyboardButton('Редагувати назви тем')
    rmk.row(b1, b2, b0)
    await bot.send_message(message.chat.id, msg, reply_markup=rmk)


@dp.message_handler(Text(startswith='Тема'), state=Form.history)
async def topics(message: types.Message, state: FSMContext):
    await Form.topics.set()
    async with state.proxy() as qdata:
        subject_id = qdata['subject_id']

    rmk = types.reply_keyboard.ReplyKeyboardMarkup(resize_keyboard=True)
    b1 = types.reply_keyboard.KeyboardButton("Добавити нову тему")
    b2 = types.reply_keyboard.KeyboardButton("Повернутися назад")
    rmk.row(b1, b2)

    topics_list = db.get_topics(subject_id)
    # print(topics_list)
    topics_list.sort(key=lambda x: x[3])
    for topic in topics_list:
        b = types.reply_keyboard.KeyboardButton(topic[1])
        rmk.add(b)
    msg = "Оберіть тему"
    await bot.send_message(message.chat.id, msg, reply_markup=rmk)


@dp.message_handler(Text(startswith='Повернутися назад'), state=Form.topics)
async def func(message: types.Message, state: FSMContext):
    await history(message, state)


@dp.message_handler(Text(startswith='Добавити нову тему'), state=Form.topics)
async def func(message: types.Message, state: FSMContext):
    await Form.new_topic.set()
    msg = "Введіть назву теми, також, при необхідності, введіть через абзац пріоритет показу(за замовчуванням добавл" \
          "яється в самий кінець)\nЩоб скасувати операцію напишіть Cancel або Відміна(з великої)"
    rmk = types.reply_keyboard.ReplyKeyboardMarkup(resize_keyboard=True)
    b1 = types.reply_keyboard.KeyboardButton("Відміна")
    rmk.add(b1)
    await bot.send_message(message.chat.id, msg, reply_markup=rmk)


@dp.message_handler(Text(startswith='Відміна'), state=Form.new_topic)
@dp.message_handler(Text(startswith='Досить'), state=Form.new_topic)
@dp.message_handler(Text(startswith='Cancel'), state=Form.new_topic)
async def func(message: types.Message, state: FSMContext):
    await topics(message, state)


@dp.message_handler(Text(startswith="Добавити ще одну"), state=Form.new_topic)
@dp.message_handler(Text(startswith="Спробувати ще раз"), state=Form.new_topic)
async def func(message: types.Message, state: FSMContext):
    pass


@dp.message_handler(state=Form.new_topic)
async def func(message: types.Message, state: FSMContext):
    async with state.proxy() as qdata:
        subject_id = qdata['subject_id']

    text = message.text.split("\n")
    topic_name = text[0]
    try:
        topic_priot = text[1]
    except:
        topics_list = db.get_topics(subject_id)
        topic_priot = max(topics_list, key=lambda x: x[3])[3]+1

    try:
        topic_priot = int(topic_priot)
        db.add_topic(topic_name, subject_id, topic_priot)
        msgs = ['Неймовірний успіх', 'Вдала спроба!', 'Неочікувано все працює']
        rmk = types.reply_keyboard.ReplyKeyboardMarkup(resize_keyboard=True)
        b1 = types.reply_keyboard.KeyboardButton("Добавити ще одну")
        b2 = types.reply_keyboard.KeyboardButton("Досить")
        rmk.add(b1, b2)
        await bot.send_message(message.chat.id, msgs[randint(0, len(msgs)-1)], reply_markup=rmk)
    except:
        msg = "Сервер не відповідає. Сервер прийняв іслам\nПеревірте чи зробили все правильно"
        rmk = types.reply_keyboard.ReplyKeyboardMarkup(resize_keyboard=True)
        b1 = types.reply_keyboard.KeyboardButton("Спробувати ще раз")
        b2 = types.reply_keyboard.KeyboardButton("Відміна")
        rmk.add(b1, b2)
        await bot.send_message(message.chat.id, msg, reply_markup=rmk)


async def print_topic(topic_id, chat_id, state: FSMContext):
    await Form.topic.set()
    pers = db.get_pers(topic_id)
    photos = db.get_photos(topic_id)
    dates = db.get_dates(topic_id)
    async with state.proxy() as qdata:
        qdata['pers'] = pers
        qdata['photos'] = photos
        qdata['dates'] = dates
    # print(photos)
    k1 = len(pers)
    k2 = len(photos)
    k3 = len(dates)

    rmk = types.reply_keyboard.ReplyKeyboardMarkup(resize_keyboard=True)
    msg = ""
    if k1 + k2 + k3 == 0:
        msg += "В даній темі питань немає\n"
    else:
        b = types.reply_keyboard.KeyboardButton("Випадкове питання")
        rmk.add(b)
    if k1 > 0:
        b = types.reply_keyboard.KeyboardButton("Персоналії")
        rmk.add(b)
        msg += f"Кількість питань по персонажам: {k1}\n"
    if k2 > 0:
        b = types.reply_keyboard.KeyboardButton("Візуальні питання")
        rmk.add(b)
        msg += f"Кількість візуальних питань: {k2}\n"
    if k3 > 0:
        b = types.reply_keyboard.KeyboardButton("Дати")
        rmk.add(b)
        msg += f"Кількість питань по датах: {k3}\n"
    msg += "Оберіть дію"
    b1 = types.reply_keyboard.KeyboardButton("Повернутися до списку тем")
    b2 = types.reply_keyboard.KeyboardButton("Добавити нове запитання")
    b3 = types.reply_keyboard.KeyboardButton("Редагувати запитання")
    rmk.row(b1, b2, b3)
    await bot.send_message(chat_id, msg, reply_markup=rmk)


@dp.message_handler(state=Form.topics)
async def func(message: types.Message, state: FSMContext):
    async with state.proxy() as qdata:
        subject_id = qdata['subject_id']

    topic = message.text
    # print(topic)
    topic_id = db.get_topic(topic, subject_id)[0][0]
    # print(topic_id)
    async with state.proxy() as qdata:
        qdata['topic_id'] = topic_id
    await print_topic(topic_id, message.chat.id, state)


@dp.message_handler(Text(startswith='Випадкове питання'), state=Form.topic)
async def func(message: types.Message, state: FSMContext):
    async with state.proxy() as qdata:
        questions = qdata['pers'] + qdata['photos'] + qdata['dates']
    random1 = randint(0, len(questions)-1)

    question = questions[random1]

    rmk = types.inline_keyboard.InlineKeyboardMarkup()
    b1 = types.inline_keyboard.InlineKeyboardButton(text="Відповідь", callback_data=f'ansr_{random1}')
    rmk.add(b1)
    msg = f"{question[2]}"
    await bot.send_message(message.chat.id, msg, reply_markup=rmk)


@dp.callback_query_handler(Text(startswith='ansr'), state="*")
async def func(callback: types.callback_query, state: FSMContext):
    data = callback.data.split('_')
    index = int(data[1])
    async with state.proxy() as qdata:
        questions = qdata['pers'] + qdata['photos'] + qdata['dates']
    ans = questions[index][1]
    text = f'{callback.message.text}\n\n<b>{ans}</b>'
    await callback.message.edit_text(text)
    await callback.answer()


@dp.message_handler(Text(startswith='Персоналії'), state=Form.topic)
async def func(message: types.Message, state: FSMContext):
    await set_q('pers', state, message)


@dp.message_handler(Text(startswith='Візуальні питання'), state=Form.topic)
async def func(message: types.Message, state: FSMContext):
    await set_q('photos', state, message)


@dp.message_handler(Text(startswith='Дати'), state=Form.topic)
async def func(message: types.Message, state: FSMContext):
    await set_q('dates', state, message)


async def set_q(q_type, state: FSMContext, message):
    async with state.proxy() as qdata:
        questions = qdata[q_type]

    random.shuffle(questions)

    for q in questions:
        rmk = types.inline_keyboard.InlineKeyboardMarkup()
        b1 = types.inline_keyboard.InlineKeyboardButton(text="Відповідь", callback_data=f'ans_{q_type}_{q[0]}')
        rmk.add(b1)
        msg = f"{q[2]}"
        await bot.send_message(message.chat.id, msg, reply_markup=rmk)


@dp.callback_query_handler(Text(startswith='ans'), state="*")
async def func(callback: types.callback_query, state: FSMContext):
    data = callback.data.split('_')
    q_type = data[1]
    q_id = int(data[2])

    ans = db.get_answer(q_type, q_id)[0][1]

    text = f'{callback.message.text}\n\n<b>{ans}</b>'

    await callback.message.edit_text(text)
    await callback.answer()


@dp.message_handler(Text(startswith='Повернутися до списку тем'), state=Form.topic)
async def func(message: types.Message, state: FSMContext):
    await topics(message, state)


@dp.message_handler(Text(startswith='Добавити нове запитання'), state=Form.topic)
async def func(message: types.Message, state: FSMContext):
    await Form.add_q.set()
    rmk = types.reply_keyboard.ReplyKeyboardMarkup(resize_keyboard=True)
    b1 = types.reply_keyboard.KeyboardButton("Персоналії")
    b2 = types.reply_keyboard.KeyboardButton("Візуальне")
    b3 = types.reply_keyboard.KeyboardButton("Дата")
    b4 = types.reply_keyboard.KeyboardButton("Верніть мене!")
    rmk.row(b1, b2, b3, b4)
    msg = "Виберіть тип питання"
    await bot.send_message(message.chat.id, msg, reply_markup=rmk)


@dp.message_handler(Text(startswith='Верніть мене!'), state=Form.add_q)
@dp.message_handler(Text(startswith='Верніть мене!'), state=Form.edit_q)
async def func(message: types.Message, state: FSMContext):
    async with state.proxy() as qdata:
        topic_id = qdata['topic_id']
    await print_topic(topic_id, message.chat.id, state)


async def important(message: types.Message, state: FSMContext):
    await Form.cin_new_q.set()
    rmk = types.reply_keyboard.ReplyKeyboardMarkup(resize_keyboard=True)
    b = types.reply_keyboard.KeyboardButton("Відбій")
    rmk.add(b)
    msg = "Введіть запитання і через абзац відповідь"
    await bot.send_message(message.chat.id, msg, reply_markup=rmk)


@dp.message_handler(state=Form.add_q)
async def func(message: types.Message, state: FSMContext):
    if message.text.startswith("Персоналії"):
        t = 'pers'
    elif message.text.startswith("Візуальне"):
        t = 'photos'
    elif message.text.startswith("Дата"):
        t = 'dates'
    else:
        t = 'da blia'
    async with state.proxy() as qdata:
        qdata['type'] = t
    await important(message, state)


@dp.message_handler(Text(startswith='Відбій'), state=Form.cin_new_q)
async def func(message: types.Message, state: FSMContext):
    async with state.proxy() as qdata:
        topic_id = qdata['topic_id']
    await print_topic(topic_id, message.chat.id, state)


@dp.message_handler(state=Form.cin_new_q)
async def func(message: types.Message, state: FSMContext):
    async with state.proxy() as qdata:
        t = qdata['type']
        topic_id = qdata['topic_id']
    data = message.text.split('\n')
    q = data[0]
    ans = data[1]
    rmk = types.reply_keyboard.ReplyKeyboardMarkup(resize_keyboard=True)
    b = types.reply_keyboard.KeyboardButton("Відбій")
    rmk.add(b)

    try:
        if t == 'pers':
            db.add_pers(ans, q, topic_id)
        elif t == 'photos':
            db.add_photo(ans, q, topic_id)
        elif t == 'dates':
            db.add_date(q, ans, topic_id)
        msgs = ['Як же ти харош', 'Як ти це робиш?', '11/10', 'Чомусь все працює..']
    except:
        msgs = ['Сервер дед інсайд', 'Трапилась халепа', 'Я тебе ніколи не покину... А ні, покину(невдала спроба)']
    r1 = randint(0, len(msgs))
    await bot.send_message(message.chat.id, msgs[r1], reply_markup=rmk)


@dp.message_handler(Text(startswith='Редагувати запитання'), state=Form.topic)
async def func(message: types.Message, state: FSMContext):
    await Form.edit_q.set()
    rmk = types.reply_keyboard.ReplyKeyboardMarkup(resize_keyboard=True)
    b1 = types.reply_keyboard.KeyboardButton("Персоналії")
    b2 = types.reply_keyboard.KeyboardButton("Візуальне")
    b3 = types.reply_keyboard.KeyboardButton("Дата")
    b4 = types.reply_keyboard.KeyboardButton("Верніть мене!")
    rmk.row(b1, b2, b3, b4)
    msg = "Виберіть тип запитань"
    await bot.send_message(message.chat.id, msg, reply_markup=rmk)


@dp.message_handler(state=Form.edit_q)
async def func(message: types.Message, state: FSMContext):
    if message.text.startswith("Персоналії"):
        t = 'pers'
    elif message.text.startswith("Візуальне"):
        t = 'photos'
    elif message.text.startswith("Дата"):
        t = 'dates'
    else:
        t = 'da blia'

    async with state.proxy() as qdata:
        questions = qdata[t]

    for q in questions:
        rmk = types.inline_keyboard.InlineKeyboardMarkup()
        b1 = types.inline_keyboard.InlineKeyboardButton(text="Редактувати питання", callback_data=f'edit_q_{t}_{q[0]}')
        b2 = types.inline_keyboard.InlineKeyboardButton(text="Редактувати відповідь",
                                                        callback_data=f'edit_ans_{t}_{q[0]}')
        b3 = types.inline_keyboard.InlineKeyboardButton(text="Видалити", callback_data=f'edit_del_{t}_{q[0]}')
        rmk.row(b1, b2, b3)
        msg = f"{q[2]}\n\n{q[1]}"
        await bot.send_message(message.chat.id, msg, reply_markup=rmk)


@dp.callback_query_handler(Text(startswith='edit'), state=Form.edit_q)
async def func(callback: types.callback_query, state: FSMContext):
    data = callback.data.split('_')
    action = data[1]
    t = data[2]
    q_id = int(data[3])
    async with state.proxy() as qdata:
        qdata['t'] = t
        qdata['q_id'] = q_id
        qdata['m'] = callback.message

    if action == 'q':
        msg = "Впишіть нове запитання:"
        await Form.edit_q_q.set()
    elif action == 'ans':
        msg = "Впишіть нову відповідь:"
        await Form.edit_q_ans.set()
    else:
        msg = "Ок"
        db.update_q_topic(t, q_id, -1)
        await bot.delete_message(callback.message.chat.id, callback.message.message_id)

    await bot.send_message(callback.message.chat.id, msg)
    await callback.answer()


@dp.message_handler(state=Form.edit_q_q)
async def func(message: types.Message, state: FSMContext):
    await Form.edit_q.set()
    async with state.proxy() as qdata:
        t = qdata['t']
        q_id = qdata['q_id']
        m = qdata['m']
    db.update_q_q(t, q_id, message.text)

    rmk = types.inline_keyboard.InlineKeyboardMarkup()
    b1 = types.inline_keyboard.InlineKeyboardButton(text="Редактувати питання", callback_data=f'edit_q_{t}_{q_id}')
    b2 = types.inline_keyboard.InlineKeyboardButton(text="Редактувати відповідь",
                                                    callback_data=f'edit_ans_{t}_{q_id}')
    b3 = types.inline_keyboard.InlineKeyboardButton(text="Видалити", callback_data=f'edit_del_{t}_{q_id}')
    rmk.row(b1, b2, b3)
    await m.edit_text(message.text, reply_markup=rmk)


@dp.message_handler(state=Form.edit_q_ans)
async def func(message: types.Message, state: FSMContext):
    await Form.edit_q.set()
    async with state.proxy() as qdata:
        t = qdata['t']
        q_id = qdata['q_id']
        m = qdata['m']
    db.update_q_ans(t, q_id, message.text)

    rmk = types.inline_keyboard.InlineKeyboardMarkup()
    b1 = types.inline_keyboard.InlineKeyboardButton(text="Редактувати питання", callback_data=f'edit_q_{t}_{q_id}')
    b2 = types.inline_keyboard.InlineKeyboardButton(text="Редактувати відповідь",
                                                    callback_data=f'edit_ans_{t}_{q_id}')
    b3 = types.inline_keyboard.InlineKeyboardButton(text="Видалити", callback_data=f'edit_del_{t}_{q_id}')
    rmk.row(b1, b2, b3)
    await m.edit_text(message.text, reply_markup=rmk)


@dp.message_handler(Text(startswith='Математика'), state=Form.math)
@dp.message_handler(Text(startswith='Математика'), state=None)
async def func(message: types.Message, state: FSMContext):
    await Form.math.set()
    await bot.send_message(message.chat.id, "1234")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
