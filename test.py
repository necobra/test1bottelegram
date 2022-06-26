from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from random import randint
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State

bot = Bot(token='5502925067:AAGHrx-77qnydu_xcb9XE8vMaCVEpu4KKQA', parse_mode='html')
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


class Form(StatesGroup):
    ans = State()
    ans_user = State()


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
async def test2(message: types.Message, state: FSMContext):
    async with state.proxy() as qdata:
        ans = qdata['ans']
    if not ans == int(message.text):
        msg = f"Правильный ответ: {ans}"
    else:
        msg = 'Верно'
    await bot.send_message(message.from_user.id, msg, reply_to_message_id=message.message_id)
    await state.finish()

if __name__ == '__main__':
    executor.start_polling(dp)
