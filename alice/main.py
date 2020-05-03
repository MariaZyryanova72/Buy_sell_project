import logging
import json

from data import db_session
from data.alice_users import AliceUser
from const import *

logging.basicConfig(level=logging.INFO)
sessionStorage = {}


def dialog_alice(request):
    logging.info(f'Request: {request.json!r}')
    response = {
        'session': request.json['session'],
        'version': request.json['version'],
        'response': {
            'end_session': False
        }
    }
    handle_dialog(response, request.json)
    logging.info(f'Response: {response!r}')
    return json.dumps(response)


def handle_dialog(res, req):
    res['response']['end_session'] = False
    user_id = req['session']['user_id']

    if req['session']['new']:
        res['response']['buttons'] = []
        session = db_session.create_session()
        user = session.query(AliceUser).filter(AliceUser.id_user == user_id).first()
        sessionStorage[user_id] = {
            'commands': ['Куплю', 'Продам', 'Помощь'],
            'current_dialog_id': '',
            'first_name': None
        }
        if user:
            res['response']['text'] = f'Привет, { user.name }!\n' \
                                      f'Что хотите? Купить или продать?'
            sessionStorage[user_id]['first_name'] = user.name
            res['response']['buttons'] = [
                {'title': "Куплю", 'hide': True},
                {'title': "Продам", 'hide': True},
                {'title': "Помощь", 'hide': True}
            ]
            return
        else:
            res['response']['text'] = 'Привет! Назови свое имя!'
            return

    if sessionStorage[user_id]['first_name'] is None:
        first_name = get_first_name(req)
        if first_name is None:
            res['response']['text'] = \
                'Не расслышала имя. Повтори, пожалуйста!'
        else:
            sessionStorage[user_id]['first_name'] = first_name[0].upper() + first_name[1:]
            add_user_db(sessionStorage[user_id]['first_name'], user_id)
            res['response']['text'] = f"Приятно познакомиться, { sessionStorage[user_id]['first_name'] }!\n" \
                                      f"'Что хотите? Купить или продать?"
            res['response']['buttons'] = [
                {'title': "Куплю", 'hide': True},
                {'title': "Продам", 'hide': True},
                {'title': "Помощь", 'hide': True}
            ]
            return
    command = req['request']['original_utterance']
    if command == 'Помощь' and command in sessionStorage[user_id]['commands']:
        help_alice(res, req)

    elif command == 'Куплю' and command in sessionStorage[user_id]['commands']:
        sessionStorage[user_id]['commands'] = ['Продам', 'Помощь', 'В начало']
        res['response']['text'] = 'Куплю'
        sessionStorage[user_id]['current_dialog_id'] = 'Buy'

    elif command == 'Продам' and command in sessionStorage[user_id]['commands']:
        sessionStorage[user_id]['commands'] = ['Куплю', 'Помощь', 'В начало']
        res['response']['text'] = 'Продам'
        sessionStorage[user_id]['current_dialog_id'] = 'Sel'

    elif command == 'В начало' and command in sessionStorage[user_id]['commands']:
        sessionStorage[user_id]['commands'] = ['Куплю', 'Продам', 'Помощь']
        sessionStorage[user_id]['current_dialog_id'] = ''
        res['response']['text'] = 'Что хотите? Купить или продать?'
    alice_buttons(res, req)


def alice_buttons(res, req):
    user_id = req['session']['user_id']
    if sessionStorage[user_id]['current_dialog_id'] == '':
        res['response']['buttons'] = [
            {'title': "Куплю", 'hide': True},
            {'title': "Продам", 'hide': True},
            {'title': "Помощь", 'hide': True}
        ]

    elif sessionStorage[user_id]['current_dialog_id'] == 'Buy':
        res['response']['buttons'] = [
            {'title': "Продам", 'hide': True},
            {'title': "В начало", 'hide': True},
            {'title': "Помощь", 'hide': True}
        ]

    elif sessionStorage[user_id]['current_dialog_id'] == 'Sel':
        res['response']['buttons'] = [
            {'title': "Куплю", 'hide': True},
            {'title': "В начало", 'hide': True},
            {'title': "Помощь", 'hide': True}
        ]


def help_text(lst):
    return 'Команды, которые я понимаю:\n' + '\n'.join(lst)


def help_alice(res, req):
    user_id = req['session']['user_id']
    if sessionStorage[user_id]['current_dialog_id'] == '':
        res['response']['text'] = help_text([BUY_TEXT, SELL_TEXT])

    if sessionStorage[user_id]['current_dialog_id'] == 'Buy':
        res['response']['text'] = help_text([SELL_TEXT, START_DIALOG_TEXT])

    if sessionStorage[user_id]['current_dialog_id'] == 'Sel':
        res['response']['text'] = help_text([BUY_TEXT, START_DIALOG_TEXT])


def get_first_name(req):
    for entity in req['request']['nlu']['entities']:
        if entity['type'] == 'YANDEX.FIO':
            return entity['value'].get('first_name', None)


def add_user_db(name, id_user):
    user = AliceUser()
    user.name = name
    user.id_user = id_user
    session = db_session.create_session()
    session.add(user)
    session.commit()
