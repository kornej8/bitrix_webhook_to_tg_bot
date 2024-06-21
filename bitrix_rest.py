import requests
import json
from config_parser import get_from_global_config
from datetime import datetime, timedelta


link = get_from_global_config('root_link')
root_token = get_from_global_config('root_rest_token')

r = f'https://{link}/rest/50/{root_token}/tasks.task.add'

# all_tasks = dict(json.loads(requests.get(r).text))
#
# for i in all_tasks['result']['tasks']:
#     print(i['description'])


"""Добавляет задачу"""
# r = f'https://{link}/rest/50/{root_token}/tasks.task.add'
# data = {'fields' : {'TITLE': 'Задача', 'CREATED_BY': 50, 'RESPONSIBLE_ID' : 50}}
#
#
# set_task = requests.post(r, json = data)
# print(set_task.text)

def push_bitrix_task(data, telegram_id):
    r = f'https://{link}/rest/50/{root_token}/tasks.task.add'
    fields = data.get(str(telegram_id)).get('set_task')
    json = {'fields': {'TITLE': fields.get('TITLE', 'Задача'),
                       'CREATED_BY': int(fields.get('CREATED_BY_ID')),
                       'RESPONSIBLE_ID': int(fields.get('RESPONSIBLE_ID_ID')),
                       'DESCRIPTION' : fields.get('DESCRIPTION'),
                       'END_DATE_PLAN': (datetime.now() + timedelta(days = fields.get('DEADLINE', 3))).strftime('%Y-%m-%dT19:00:00+03:00'),
                       'DEADLINE': (datetime.now() + timedelta(days = fields.get('DEADLINE', 3))).strftime('%Y-%m-%dT19:00:00+03:00')
                      }}

    set_task = requests.post(r, json=json)
    if str(set_task.status_code) == '200':
        return True
    return False

def get_user_by_name(row, callback):
    r_users = f'https://{link}/rest/50/{root_token}/user.search'
    if len(row.split()) == 1:
        data = {'FILTER': {'NAME': row}}
        ans = json.loads(requests.post(r_users, json = data).text)['result']
        if len(ans) == 1:
            d = ans[0]
            return {callback : f"{d.get('LAST_NAME', '')} {d.get('NAME', '')} {d.get('SECOND_NAME', '')}",
                    f'{callback}_ID': d.get('ID')}
        elif len(ans) > 1:
            data = []
            for d in ans:
                data.append({callback : f"{d.get('LAST_NAME', '')} {d.get('NAME', '')} {d.get('SECOND_NAME', '')}",
                    f'{callback}_ID': d.get('ID')})
            return data
        else:
            return 'Сотрудник не найден'
    else:
        data = {'FILTER': {'NAME': row.split()[0], 'LAST_NAME': row.split()[1]}}
        ans = json.loads(requests.post(r_users, json=data).text)['result']
    # for i in ans['result']:
    #     print(i['ID'], i.get('NAME'), i.get('LAST_NAME'))



#
# FILTER	Массив может содержать поля в любом сочетании:
# NAME - имя
# LAST_NAME - фамилия

# r_s = f'https://{link}/rest/50/{root_token}/user.search'
# data = {'FILTER' : {'LAST_NAME': 'Марина'}}
#
#
# get_user = requests.post(r_s, json = data)
# print(get_user.text)