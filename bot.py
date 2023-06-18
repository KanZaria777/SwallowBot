import time
import logging

from aiogram import Bot, Dispatcher, executor, types


TOKEN = ""
MSG = "Поиграл ли ты сегодня в жабку, {}?"
CODE_WORDS = ['Моя жаба', 'Завершить работу', 'Отправить жабу на работу', '@toadbot Поход в столовую',
              '@toadbot Работа крупье', '@toadbot Работа грабитель']

bot = Bot(token=TOKEN)
dp = Dispatcher(bot=bot)


@dp.message_handler(commands=['start'])
async def start_handler(message: types.Message):
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    user_full_name = message.from_user.full_name
    logging.info(f'{user_id=} {user_full_name=} {time.asctime()}')
    await message.reply(f"Привет, {user_full_name}!")

    for i in range(1):
        time.sleep(86400)

        await bot.send_message(user_id, MSG.format(user_name))



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
    
