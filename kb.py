from telebot import types

def start_kb():

    keyboard = types.InlineKeyboardMarkup(row_width=1)

    keyboard.row(
        types.InlineKeyboardButton(text = 'Поставить задачу', callback_data='set_task'),
        )

    return keyboard

def task_kb():

    keyboard = types.InlineKeyboardMarkup(row_width=1)
    buttons = [types.InlineKeyboardButton(text='Указать поставновщика (обязательно)', callback_data='CREATED_BY'),
        types.InlineKeyboardButton(text='Указать исполнителя (обязательно)', callback_data='RESPONSIBLE_ID'),
        types.InlineKeyboardButton(text='Указать заголовок (обязательно)', callback_data='TITLE'),
        types.InlineKeyboardButton(text='Указать описание', callback_data='DESCRIPTION'),
        types.InlineKeyboardButton(text='Указать количество дней на выполнение задачи', callback_data='DEADLINE'),
        ]

    keyboard.add(*buttons)

    return keyboard