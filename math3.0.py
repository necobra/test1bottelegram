from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from random import randint
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher.filters import Text

bot = Bot(token='5502925067:AAGHrx-77qnydu_xcb9XE8vMaCVEpu4KKQA', parse_mode='html')
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


class Form(StatesGroup):
    ans = State()
    ans_user = State()


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    rmk = types.reply_keyboard.ReplyKeyboardMarkup(resize_keyboard=True)
    b1 = types.reply_keyboard.KeyboardButton('/new_problem')
    b2 = types.reply_keyboard.KeyboardButton('/history_p')
    b3 = types.reply_keyboard.KeyboardButton('/history_y')
    b4 = types.reply_keyboard.KeyboardButton('/history_pers')
    rmk.row(b1, b2, b3, b4)
    msg = "Меню"
    await bot.send_message(message.chat.id, msg, reply_markup=rmk)


@dp.message_handler(commands=['new_problem'])
async def test(message: types.Message, state: FSMContext):
    int1 = randint(11, 99)
    int2 = randint(11, 99)
    msg = f"{int1} * {int2} ="
    await bot.send_message(message.from_user.id, msg)
    async with state.proxy() as qdata:
        qdata['ans'] = int1*int2
    await Form.ans_user.set()


@dp.message_handler(state=Form.ans_user)
async def test(message: types.Message, state: FSMContext):
    if not await check_cond(message, state):
        return 0
    async with state.proxy() as qdata:
        ans = qdata['ans']
    if not ans == int(message.text):
        msg = f"Правильный ответ: {ans}"
    else:
        msg = f'Верно'
    await bot.send_message(message.from_user.id, msg, reply_to_message_id=message.message_id)
    await state.finish()


async def check_cond(message, state: FSMContext):
    text = message.text
    if text == '/history_p':
        await state.finish()
        await history_p(message)
        return 0
    elif text == '/history_y':
        await state.finish()
        await history_y(message)
        return 0
    return 1


@dp.message_handler(commands=['history_p'])
async def history_p(message: types.Message):
    int1 = randint(1, 24)
    names = ['Шептицький', 'Кость-Левицький', 'Галущинський', 'Грушевський', 'Шептицький', 'Галущинський',
             'Скоропадський', 'Скоропадський', 'Винниченко', 'Винниченко', 'Петлюра', 'Петлюра', 'Петрушевич',
             'Петрушевич', 'Григорій Петровський', 'Раховський', 'Раховський', 'Нестор Махно', 'Дмитро Левицький',
             'Коновалець', 'Коновалець', 'Мельник', 'український апостол', 'Августин Волошин']
    # print(len(names))
    rmk = types.inline_keyboard.InlineKeyboardMarkup()
    b1 = types.inline_keyboard.InlineKeyboardButton(text="Відповідь", callback_data=f'portrait_{names[int1-1]}')
    rmk.add(b1)
    await bot.send_photo(message.from_user.id, caption='', photo=open(f'portraits/{int1}.png', 'rb'), reply_markup=rmk)


@dp.callback_query_handler(Text(startswith='portrait'))
async def test(callback: types.callback_query):
    name = callback.data[9:]
    await callback.message.edit_caption(name)
    await callback.answer()


@dp.message_handler(commands=['history_pers'])
async def history_p(message: types.Message):
    int1 = randint(1, 10)
    names = ['Тарас Бульба-Боровець', 'Мельник', 'Бандера', 'Шухевич', 'Кирило Осьмак', 'Олена Теліга',
             'Іван Багряний (Іван Лозов’ягін)', 'Олексій Берест', 'Іван Кожедуб', 'Амет-Хан Султан']
    # print(len(names))
    rmk = types.inline_keyboard.InlineKeyboardMarkup()
    b1 = types.inline_keyboard.InlineKeyboardButton(text="Відповідь", callback_data=f'pers_{names[int1-1]}')
    rmk.add(b1)
    await bot.send_photo(message.from_user.id, caption='', photo=open(f'pers/{int1}.png', 'rb'), reply_markup=rmk)


@dp.callback_query_handler(Text(startswith='pers'))
async def test(callback: types.callback_query):
    name = callback.data[5:]
    await callback.message.edit_caption(name)
    await callback.answer()


@dp.message_handler(commands=['history_y'])
async def history_y(message: types.Message):
    event = ['Галицька битва', 'Горлицька битва', 'ЗУР', 'УСС основано',
             'Брусиловський прорив', 'УЦР', 'І універсал', 'ІІ універсал', 'ІІІ універсал',
             'IV універсал', 'Берестейський мирний договір', 'конституція УНР', 'прихід до влади Скоропадського',
             'грамота Скоропадського про вступ до Всерос фед народів', 'створення директорії УНР',
             'прихід до влади директорії', 'проголошення самостійнойсті ЗУНР', 'Акт злуки', 'Чортківська офензива',
             'Київська катастрофа', 'Перший зимовий похід', '3 прихід більшовиків(після Денікена)',
             'Варшавський договір',
             'Ризький мирний договір', '2 зимовий похід', "1 Всесоюзний з'їзд",
             'ЛІКНЕП СРСР', 'коренізація УРСР', 'НЕП', 'перший голод УРСР',
             'ств незал афтокифальної прав церкви в Україні',
             'ідея на індустралізацію', 'часи модернізації', "перша п'ятирічка", 'перехід до суцільної колетивізації',
             '2 голодомор в Україні', 'Шахтинська справа, справа над СВУ, розстріляне відродження',
             'рік великого перелому']
    date = ['23 серпня 14р', 'травень 15р', '5 травня 15р', 'серпень 14р',
            'травень-червень 16р', '17 березня 17р', '23 червня 17р', '16 липень 17р', '20 листопад 17р',
            '22 січня 18р', '9 лютого 18р', '29 квітня 18р', '30 квітня 18р',
            '14 листопада 18р', '14 листопада 18р',
            '18 грудня 18р', '13 листопада', '22 січня 19р', 'червень 19р',
            '30-31 серпня 19р', '6 грудня 19р - 6 травня 20р', 'грудень 19р',
            'квітень 20р',
            '18 березня 21р', 'листопад 21р', '30 грудня 22р',
            'поч 1920', '23р', '21-28рр', '21-23рр',
            '21р',
            '1925р', 'кін 20 - 30-ті роки', '1928-1932', '1929р',
            '1932-1933рр', '1928р, 1930р, 1936-1938рр',
            '1929р']
    int1 = randint(0, len(date)-1)
    # print(len(event))
    # print(len(date))
    rmk = types.inline_keyboard.InlineKeyboardMarkup()
    b1 = types.inline_keyboard.InlineKeyboardButton(text="Відповідь", callback_data=f'date_ans_{date[int1]}')
    rmk.add(b1)

    await bot.send_message(message.from_user.id, f'<b>{event[int1]}</b>', reply_markup=rmk)


@dp.callback_query_handler(Text(startswith='portrait'))
async def test(callback: types.callback_query):
    name = callback.data[9:]
    await callback.message.edit_caption(name)
    await callback.answer()


@dp.callback_query_handler(Text(startswith='date_ans'))
async def test(callback: types.callback_query):
    name = callback.data[9:]
    text = f'<b>{callback.message.text}</b>\n{name}'
    await callback.message.edit_text(text)
    await callback.answer()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
