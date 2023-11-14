from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardMarkup

#общая клавиатура
main = ReplyKeyboardMarkup(resize_keyboard=True)
# main.add('Толик').add('Андрей').add('Костян')
main.add('Толик', 'Андрей', 'Костян')

# клавиатура админа
main_admin = ReplyKeyboardMarkup(resize_keyboard=True)
main_admin.add('Толик', 'Андрей', 'Костян', 'Админка')

#клавиатура самой админ панели
admin_panel = ReplyKeyboardMarkup(resize_keyboard=True)
admin_panel.add('Статистика')

social_links = InlineKeyboardMarkup(row_widht=2)
social_links.add(InlineKeyboardMarkup(text='Инфо', callback_data='Клоун'))