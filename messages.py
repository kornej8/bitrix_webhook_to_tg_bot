from datetime import datetime, timedelta



def set_task_message(params = {}):
    text = f"""
<b>Название задачи</b>: {params.get('TITLE', '')}

<b>Описание задачи</b>: {params.get('DESCRIPTION', '')}

<b>Постановщик</b>: {params.get('CREATED_BY', '')}
<b>Исполнитель</b>: {params.get('RESPONSIBLE_ID', '')}
<b>Крайний срок</b>: {(datetime.now() + timedelta(days = 3)).strftime('%d.%m.%Y')}
"""
    return text


messages = {
    'set_task_message' : set_task_message
}