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



def get_bitrix_user_by_name(message, draft_task_message_id, bot, telegram_id, callback):
    global data_manager

    try:
        line = get_user_by_name(message.text)
        raise Exception
    except:
        line = message.text

    bot.delete_message(chat_id=telegram_id, message_id=message.message_id)
    bot.edit_message_text(message_id=draft_task_message_id,
                          chat_id=telegram_id,
                          text=messages.get('set_task_message')({callback : line}),
                          reply_markup=None, parse_mode='HTML')

    data_manager[str(telegram_id)]['set_task'][callback] = line


def created_by(bot, query, **kwargs):
    callback = query.data
    draft_task_message_id = query.message.id
    telegram_id = query.from_user.id
    bot.edit_message_text(message_id=draft_task_message_id,
                          chat_id= telegram_id,
                          text = messages.get('set_task_message')(),
                          reply_markup=None, parse_mode='HTML')
    msg = bot.send_message(chat_id= query.from_user.id, text='Введите имя постановщика задачи:')
    bot.register_next_step_handler(msg, get_bitrix_user_by_name, draft_task_message_id, bot, telegram_id, callback)


def created_by(bot, query, **kwargs):
    callback = query.data
    draft_task_message_id = query.message.id
    telegram_id = query.from_user.id
    bot.edit_message_text(message_id=draft_task_message_id,
                          chat_id= telegram_id,
                          text = messages.get('set_task_message')(),
                          reply_markup=None, parse_mode='HTML')
    msg = bot.send_message(chat_id= query.from_user.id, text='Введите имя постановщика задачи:')
    bot.register_next_step_handler(msg, get_bitrix_user_by_name, draft_task_message_id, bot, telegram_id, callback)


def title(bot, query, **kwargs):
    callback = query.data
    draft_task_message_id = query.message.id
    telegram_id = query.from_user.id
    bot.edit_message_text(message_id=draft_task_message_id,
                          chat_id= telegram_id,
                          text = messages.get('set_task_message')(),
                          reply_markup=None, parse_mode='HTML')
    msg = bot.send_message(chat_id= query.from_user.id, text='Введите название задачи:')
    m = bot.register_next_step_handler(msg, get_bitrix_user_by_name, draft_task_message_id, bot, telegram_id, callback)




callbacks = {
    'set_task': set_task,
    'CREATED_BY': created_by,
    'TITLE': title
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