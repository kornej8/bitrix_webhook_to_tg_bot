from bitrix_rest import *
from kb import *
from messages import messages

data_manager = {}


def set_task(bot, query, **kwargs):
    global data_manager
    if query.from_user.id not in data_manager:
        data_manager[str(query.from_user.id)] = {'set_task': {}}

    msg = bot.edit_message_text(message_id = query.message.id,
                          chat_id=query.from_user.id,
                          text=messages.get('set_task_message')(),
                          reply_markup = task_kb(), parse_mode='HTML')

def push_task(bot, query, **kwargs):
    global data_manager
    telegram_id = query.from_user.id
    try:
        status = push_bitrix_task(data_manager, telegram_id)
    except:
        status = False

    del data_manager[str(telegram_id)]

    if status:
        bot.edit_message_text(message_id=query.message.id,
                              chat_id=query.from_user.id,
                              text ='Задача <b>успешно</b> поставлена!',
                              parse_mode = 'HTML')
    else:
        bot.edit_message_text(message_id=query.message.id,
                              chat_id=query.from_user.id,
                              text='Не удалось поставить задачу. Проверьте правильность введеной информации.',
                              parse_mode='HTML')


def get_bitrix_user_by_name(message, draft_task_message_id, bot, telegram_id, callback, message_id_bot, for_delete = True):
    global data_manager

    line = get_user_by_name(message.text, callback)

    if isinstance(line, dict):
        data_manager[str(telegram_id)]['set_task'][callback + '_ID'] = line.get(callback + "_ID")
        data_manager[str(telegram_id)]['set_task'][callback] = line.get(callback)
        if for_delete:
            bot.delete_message(chat_id=telegram_id, message_id=message.message_id)
            bot.delete_message(chat_id=telegram_id, message_id=message_id_bot)

        bot.edit_message_text(message_id=draft_task_message_id,
                              chat_id=telegram_id,
                              text=messages.get('set_task_message')(data_manager.get(str(telegram_id), {}).get('set_task', {})),
                              reply_markup=task_kb(list(data_manager.get(str(telegram_id), {}).get('set_task', {}).keys())), parse_mode='HTML')



    elif isinstance(line, list):
        bot.delete_message(chat_id=telegram_id, message_id=message.message_id)
        bot.edit_message_text(message_id=message_id_bot,
                              chat_id=telegram_id,
                              text='Найдено несколько пользователей. Выберите одного:',
                              reply_markup=kb_users(line, callback))


def created_by(bot, query, **kwargs):
    callback = query.data.split(':')[0]
    draft_task_message_id = query.message.id
    telegram_id = query.from_user.id

    if not 'id' in kwargs:
        bot.edit_message_text(message_id=draft_task_message_id,
                              chat_id= telegram_id,
                              text = messages.get('set_task_message')(data_manager.get(str(telegram_id), {}).get('set_task', {})),
                              reply_markup=None, parse_mode='HTML')
        msg = bot.send_message(chat_id= query.from_user.id, text='Введите имя постановщика задачи:')
        bot.register_next_step_handler(msg, get_bitrix_user_by_name, draft_task_message_id, bot, telegram_id, callback,
                                       msg.message_id)
    else:
        print(query)
        print(kwargs.get('id'))
        data_manager[str(telegram_id)]['set_task'][callback + '_ID'] = kwargs.get('id')
        buttons = query.json['message']['reply_markup']['inline_keyboard']
        for button in buttons:
            if button.get('callback_data') == query.data:
                data_manager[str(telegram_id)]['set_task'][callback + '_ID'] = kwargs.get('id')
                break



        # data_manager[str(telegram_id)]['set_task'][callback] = line.get(callback)
        # bot.edit_message_text(message_id=draft_task_message_id,
        #                       chat_id=telegram_id,
        #                       text=messages.get('set_task_message')(
        #                           data_manager.get(str(telegram_id), {}).get('set_task', {})),
        #                       reply_markup=None, parse_mode='HTML')


def set_title(message, draft_task_message_id, bot, telegram_id, callback, message_id_bot):
    global data_manager

    line = message.text
    data_manager[str(telegram_id)]['set_task'][callback] = line


    bot.delete_message(chat_id=telegram_id, message_id=message.message_id)
    bot.delete_message(chat_id=telegram_id, message_id=message_id_bot)
    bot.edit_message_text(message_id=draft_task_message_id,
                              chat_id=telegram_id,
                              text=messages.get('set_task_message')(data_manager.get(str(telegram_id), {}).get('set_task', {})),
                              reply_markup=task_kb(list(data_manager.get(str(telegram_id), {}).get('set_task', {}).keys())), parse_mode='HTML')


def title(bot, query, **kwargs):
    global data_manager

    callback = query.data
    draft_task_message_id = query.message.id
    telegram_id = query.from_user.id
    bot.edit_message_text(message_id=draft_task_message_id,
                          chat_id= telegram_id,
                          text = messages.get('set_task_message')(data_manager.get(str(telegram_id), {}).get('set_task', {})),
                          reply_markup=None, parse_mode='HTML')
    msg = bot.send_message(chat_id= query.from_user.id, text='Введите название задачи:')
    m = bot.register_next_step_handler(msg, set_title, draft_task_message_id, bot, telegram_id, callback, msg.message_id)


def responsible_id(bot, query, **kwargs):
    callback = query.data
    draft_task_message_id = query.message.id
    telegram_id = query.from_user.id
    if kwargs.get('new', True):
        bot.edit_message_text(message_id=draft_task_message_id,
                              chat_id=telegram_id,
                              text=messages.get('set_task_message')(
                                  data_manager.get(str(telegram_id), {}).get('set_task', {})),
                              reply_markup=None, parse_mode='HTML')
        msg = bot.send_message(chat_id=query.from_user.id, text='Введите имя исполнителя задачи:')
        bot.register_next_step_handler(msg, get_bitrix_user_by_name, draft_task_message_id, bot, telegram_id, callback,
                                       msg.message_id)

def description(bot, query, **kwargs):
    global data_manager

    callback = query.data
    draft_task_message_id = query.message.id
    telegram_id = query.from_user.id
    bot.edit_message_text(message_id=draft_task_message_id,
                          chat_id=telegram_id,
                          text=messages.get('set_task_message')(
                              data_manager.get(str(telegram_id), {}).get('set_task', {})),
                          reply_markup=None, parse_mode='HTML')
    msg = bot.send_message(chat_id=query.from_user.id, text='Введите описание задачи:')
    m = bot.register_next_step_handler(msg, set_title, draft_task_message_id, bot, telegram_id, callback,
                                       msg.message_id)


def set_days(message, draft_task_message_id, bot, telegram_id, callback, message_id_bot):
    global data_manager

    line = message.text
    data_manager[str(telegram_id)]['set_task'][callback] = int(line)

    bot.delete_message(chat_id=telegram_id, message_id=message.message_id)
    bot.delete_message(chat_id=telegram_id, message_id=message_id_bot)
    bot.edit_message_text(message_id=draft_task_message_id,
                          chat_id=telegram_id,
                          text=messages.get('set_task_message')(
                              data_manager.get(str(telegram_id), {}).get('set_task', {})),
                          reply_markup=task_kb(list(data_manager.get(str(telegram_id), {}).get('set_task', {}).keys())),
                          parse_mode='HTML')


def deadline(bot, query, **kwargs):
    global data_manager

    callback = query.data
    draft_task_message_id = query.message.id
    telegram_id = query.from_user.id
    bot.edit_message_text(message_id=draft_task_message_id,
                          chat_id=telegram_id,
                          text=messages.get('set_task_message')(
                              data_manager.get(str(telegram_id), {}).get('set_task', {})),
                          reply_markup=None, parse_mode='HTML')
    msg = bot.send_message(chat_id=query.from_user.id, text='Введите количество дней на выполнение задачи:')
    m = bot.register_next_step_handler(msg, set_days, draft_task_message_id, bot, telegram_id, callback,
                                       msg.message_id)
callbacks = {
    'set_task': set_task,
    'CREATED_BY': created_by,
    'RESPONSIBLE_ID': responsible_id,
    'DESCRIPTION': description,
    'TITLE': title,
    'DEADLINE': deadline,
    'push_task': push_task
}


# bot.answer_callback_query(callback_query_id=call.id, text='Hello world')


# @bot.message_handler(commands=['start'])
# def welcome(message):
#     mesg = bot.send_message(message.chat.id,'Please send me message')
#     bot.register_next_step_handler(mesg,test)
#
#
# def test(message):
#     bot.send_message(message.chat.id,'You send me message')