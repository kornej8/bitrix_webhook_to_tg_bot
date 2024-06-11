import requests
import json
from config_parser import get_from_global_config

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


def get_user_by_name(row):
    r_users = f'https://{link}/rest/50/{root_token}/user.search'
    # ans = json.loads(requests.get(r_users).text)

    if len(row.split()) == 1:
        data = {'FILTER': {'NAME': row}}
        ans = json.loads(requests.post(r_users, json = data).text)['result']


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