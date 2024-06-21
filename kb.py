from telebot import types


def start_kb():
    keyboard = types.InlineKeyboardMarkup(row_width=1)

    keyboard.row(
        types.InlineKeyboardButton(text='Поставить задачу', callback_data='set_task'),
    )

    return keyboard


def task_kb(callbacks_list = []):
    callbacks = {'CREATED_BY': ' поставновщика (обязательно)',
                 'RESPONSIBLE_ID': ' исполнителя (обязательно)',
                 'TITLE': ' заголовок (обязательно)',
                 'DESCRIPTION': '  описание',
                 'DEADLINE': ' количество дней на выполнение задачи'}

    keyboard = types.InlineKeyboardMarkup(row_width=1)

    # buttons = [
    #     types.InlineKeyboardButton(
    #         text=f"{'Изменить' if params.get('callback') == callback else 'Указать'}{button.replace('(обязательно)', '') if params.get('callback') == callback else button}",
    #         callback_data=f"{callback + '_not_new' if params.get('callback') == callback else callback}")
    #     for callback, button in callbacks.items()
    # ]

    buttons = [
            types.InlineKeyboardButton(
                text=f"Указать {button}",
                callback_data=callback)
            for callback, button in callbacks.items() if callback not in callbacks_list
        ]
    buttons.append(types.InlineKeyboardButton(text = 'Поставить задачу', callback_data= 'push_task'))

    keyboard.add(*buttons)

    return keyboard


def kb_users(users_list, callback):
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    buttons = [types.InlineKeyboardButton(text= user.get(callback),
                                          callback_data= f"{callback}:{user.get(callback+'_ID')}")
    for user in users_list]
    print([(user.get(callback), f"{callback}:{user.get(callback+'_ID')}") for user in users_list])
    keyboard.add(*buttons)
    return keyboard
