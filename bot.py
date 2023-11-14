from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from app import keyboards as kb
from app import database as db
from dotenv import load_dotenv
import os


storage = MemoryStorage()
load_dotenv()
bot = Bot(os.getenv('TOKEN'))
dp = Dispatcher(bot=bot, storage=storage)


CODE_WORDS = ['Моя жаба', 'Завершить работу', 'Отправить жабу на работу', 'Покормить жабу', '@toadbot Поход в столовую',
              '@toadbot Работа крупье', '@toadbot Работа грабитель']



async def on_startup(_):
    await db.start_db()
    print('Успешный запуск!')


@dp.message_handler(commands=['start'])
async def start_handler(message: types.Message):
    user_id = message.from_user.id
    await db.cmd_start_db(message.from_user.id)
    await message.answer_sticker("CAACAgIAAxkBAAPuZRW6RHoFFnEUo0Bw5pfOYTOwuQEAAjUSAAJW1glIVcIkKqo_6n4wBA")
    if user_id == int(os.getenv('ADMIN_ID')):
        await message.answer(f'Приветствую', reply_markup=kb.main_admin)
    else:
        await message.answer(f'Привет {message.from_user.first_name}', reply_markup=kb.main)


@dp.message_handler(text='Админка')
async def check_admin(message: types.Message):
    if message.from_user.id == int(os.getenv('ADMIN_ID')):
        await message.reply(f'Принято {message.from_user.first_name}!', reply_markup=kb.admin_panel)
        '''
        если мы назовем функцию main_admin or admin_panel мы в первом случае лишимся стартовой панели админа(провалимся глубже
        во втором получить ошибку с вызовом JSON файла, так как передает в клавиатуры функцию, вместо клавиатуры
        '''


@dp.message_handler(text='Толик')
async def Tolik(message: types.Message):
    await message.answer_sticker('CAACAgIAAx0CbiIutgACEQJlHbgOrwMYVpVAti6mgNHCS4jeGwACPBgAAuBwGUitbvj9Z4vJWDAE')


@dp.message_handler(text='Андрей')
async def Andrey(message: types.Message):
    await message.answer_sticker('CAACAgIAAx0CbiIutgACEQRlHbgb7UqdgEZA3-8rTFu7dVfDzwACaBkAAuy6AAFIUpaMcAAB5dCmMAQ')


@dp.message_handler(text='Костян')
async def Kostyan(message: types.Message):
    await message.answer_sticker('CAACAgIAAx0CbiIutgACEQZlHbgj1ogQ2ETsc3aMsze4XH9EDQACRhcAAtPlAUi8Q4Yiot-rCjAE',
                                 reply_markup=kb.social_links)


@dp.message_handler(commands=['my_toad'])
async def delete_message(message: types.Message):
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)


# хэндлур на текстовые сообщения
@dp.message_handler(content_types=types.ContentTypes.TEXT)
async def handle_text(message: types.Message):
    # проверяем, есть ли в сообщении кодовые слова
    if any(code_word in message.text for code_word in CODE_WORDS):
        # удаляем сообщение
        await delete_message(message)

# значение которое принимает callback_query.data остается под капотом и известно, тому кто пишет код. Будто просто шнур связи.
@dp.callback_query_handler()
async def callback_query_keyboard(callback_query: types.CallbackQuery):
    if callback_query.data == 'Клоун':
        await bot.send_message(chat_id=callback_query.from_user.id, text='Этим все сказано(Клоун)')


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)
    