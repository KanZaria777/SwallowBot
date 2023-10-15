import time
import logging

from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup
from dotenv import load_dotenv
import os


load_dotenv()
bot = Bot(os.getenv('TOKEN'))
dp = Dispatcher(bot=bot)


main = ReplyKeyboardMarkup(resize_keyboard=True)
# main.add('Толик').add('Андрей').add('Костян')
main.add('Толик', 'Андрей', 'Костян')

main_admin = ReplyKeyboardMarkup(resize_keyboard=True)
main_admin.add('Толик', 'Андрей', 'Костян', 'Админка')

admin_panel = ReplyKeyboardMarkup(resize_keyboard=True)
admin_panel.add('Статистика')

CODE_WORDS = ['Моя жаба', 'Завершить работу', 'Отправить жабу на работу', '@toadbot Поход в столовую',
              '@toadbot Работа крупье', '@toadbot Работа грабитель']


@dp.message_handler(commands=['start'])
async def start_handler(message: types.Message):
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    user_full_name = message.from_user.full_name
    logging.info(f'{user_id=} {user_full_name=} {time.asctime()}')
    if user_id == int(os.getenv('ADMIN_ID')):
        await message.answer_sticker("CAACAgIAAxkBAAPuZRW6RHoFFnEUo0Bw5pfOYTOwuQEAAjUSAAJW1glIVcIkKqo_6n4wBA")
        await message.answer(f'Приветствую', reply_markup=main_admin)
    else:
        await message.answer_sticker("CAACAgIAAxkBAAPuZRW6RHoFFnEUo0Bw5pfOYTOwuQEAAjUSAAJW1glIVcIkKqo_6n4wBA")
        await message.answer(f'Привет {user_name}', reply_markup=main)


@dp.message_handler(text='Админка')
async def check_admin(message: types.Message):
    if message.from_user.id == int(os.getenv('ADMIN_ID')):
        await message.reply(f'Принято {message.from_user.first_name}!', reply_markup=admin_panel)
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
    await message.answer_sticker('CAACAgIAAx0CbiIutgACEQZlHbgj1ogQ2ETsc3aMsze4XH9EDQACRhcAAtPlAUi8Q4Yiot-rCjAE')


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


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
    