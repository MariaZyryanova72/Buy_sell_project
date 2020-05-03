import logging
import json

from data import db_session
from data.users import User


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
    res['response']['buttons'] = []

    if req['session']['new']:
        session = db_session.create_session()
        user = session.query(User).filter(User.id_user == user_id).first()
        sessionStorage[user_id] = {
            'commands': ['Куплю', 'Продам', 'Помощь', 'Настроить профиль'],
            'current_dialog_id': '',
            'settings': '',
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

    if req['request']['original_utterance'] == 'Помощь':
        help_alice(res, req)

    elif req['request']['original_utterance'] == 'Куплю':
        res['response']['text'] = 'Куплю'

    elif req['request']['original_utterance'] == 'Продам':
        res['response']['text'] = 'Продам'

    elif req['request']['original_utterance'] == 'Настроить профиль':
        res['response']['text'] = 'Настроить профиль'


def help_alice(res, req):
    user_id = req['session']['user_id']
    if sessionStorage[user_id]['current_dialog_id'] == '':
        res['response']['text'] = 'Команды, которые я понимаю:\n' \
                                  'Настроить профиль - настройка личных данных пользователя\n'


def get_first_name(req):
    for entity in req['request']['nlu']['entities']:
        if entity['type'] == 'YANDEX.FIO':
            return entity['value'].get('first_name', None)


def add_user_db(name, id_user):
    user = User()
    user.name = name
    user.id_user = id_user
    session = db_session.create_session()
    session.add(user)
    session.commit()
