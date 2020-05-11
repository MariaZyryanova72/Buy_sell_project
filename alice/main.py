import logging
import json
from threading import Thread

from flask import Flask, request

from package.const import *
import requests

logging.basicConfig(level=logging.INFO)
sessionStorage = {}

app = Flask(__name__)
app.config['SECRET_KEY'] = 'bfhdjwiskoldjEFE4GUJFTYGGG5G5G65H6G565F3222JGTHGRFDJSKE;ROJELAGTRH4TF'
URL = "http://84.201.173.242:5055/"


@app.route('/alice', methods=['POST'])
def main():
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
        user_name = requests.get(URL + '/api/v1/alice_user/' + user_id).json()

        sessionStorage[user_id] = {
            'commands': ['Куплю', 'Продам', 'Помощь'],
            'current_dialog_id': '',
            'first_name': None,
            'data_id_image': [],
            'current_ad': 0
        }
        if 'error' not in user_name:
            user_name = user_name['user']['name']
            res['response']['text'] = f'Привет, {user_name}!\n' \
                                      f'Что хотите? Купить или продать?'
            sessionStorage[user_id]['first_name'] = user_name
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
            res['response']['text'] = f"Приятно познакомиться, {sessionStorage[user_id]['first_name']}!\n" \
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
        sessionStorage[user_id]['current_dialog_id'] = 'Buy'
        res['response']['text'] = 'Что бы вы хотели купить?'

    elif command == 'Продам' and command in sessionStorage[user_id]['commands']:
        sessionStorage[user_id]['commands'] = ['Куплю', 'Помощь', 'В начало']
        res['response']['text'] = 'Продам'
        sessionStorage[user_id]['current_dialog_id'] = 'Sel'

    elif command == 'В начало' and command in sessionStorage[user_id]['commands']:
        sessionStorage[user_id]['commands'] = ['Куплю', 'Продам', 'Помощь']
        sessionStorage[user_id]['current_dialog_id'] = ''
        res['response']['text'] = 'Что хотите? Купить или продать?'

    elif sessionStorage[user_id]['current_dialog_id'] == 'Buy':
        search_data(res, req)
        if not sessionStorage[user_id]['data']:
            res['response']['text'] = 'Я ничего не нашла по вашему запросу. Введите что-нибудь другое!'
        else:
            res['response']['text'] = 'У меня есть кое-что для вас! Показать?'
            sessionStorage[user_id]['current_dialog_id'] = 'BuyData'

    elif command in ['Показать', 'Показать ещё'] and sessionStorage[user_id]['current_dialog_id'] == 'BuyData':
        buy(res, req)
        sessionStorage[user_id]['current_ad'] += 1
        if (sessionStorage[user_id]['current_ad'] == 5) or len(sessionStorage[user_id]['data']) == \
                sessionStorage[user_id]['current_ad']:
            sessionStorage[user_id]['current_dialog_id'] = ''
            sessionStorage[user_id]['commands'] = ['Продам', 'Помощь', 'В начало', 'Куплю']
            sessionStorage[user_id]['data'] = []
            sessionStorage[user_id]['data_id_image'] = []
            sessionStorage[user_id]['current_ad'] = 0

            res['response']['text'] = 'Поиск окончен. Что хотите? Купить или продать?'
        else:
            res['response']['text'] = ''
    alice_buttons(res, req)


def worker(filename, title, req):
    user_id = req['session']['user_id']
    headers = {'Authorization': 'OAuth AgAAAAAxjNpYAAT7o-FF8PGuY0mlrZN0Uxt91Wo'}
    img = requests.get(URL + '/static/img/' + filename)
    response = requests.post('https://dialogs.yandex.net/api/v1/skills/c05a819e-7883-4b1c-9ba5-e48f79b81efa/images',
                             files={'file': img.content},
                             headers=headers)
    sessionStorage[user_id]['data_id_image'].append([json.loads(response.content)['image']['id'], title])


def search_data(res, req):
    user_id = req['session']['user_id']
    q = req['request']['original_utterance']
    advertisings = requests.get(URL + '/api/v1/advertisings').json()['advertisings']
    advertisings = [ad for ad in advertisings if q in ad['title'] or q in ad['text']]
    sessionStorage[user_id]['data'] = [ad['image'] for ad in advertisings]

    for ad in advertisings:
        t = Thread(target=worker, args=(ad['image'], ad['title'], req,))
        t.start()
        t.join()


def buy(res, req):
    user_id = req['session']['user_id']
    data = sessionStorage[user_id]['data_id_image'][0]
    res['response']['card'] = {}
    res['response']['text'] = ''
    res['response']['card']['type'] = 'BigImage'
    res['response']['card']['title'] = data[1]
    res['response']['card']['image_id'] = data[0]


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

    elif sessionStorage[user_id]['current_dialog_id'] == 'BuyData':
        if sessionStorage[user_id]['current_ad'] == 0:
            res['response']['buttons'] = [
                {'title': "Показать", 'hide': True},
                {'title': "В начало", 'hide': True},
            ]
        else:
            res['response']['buttons'] = [
                {'title': "Показать ещё", 'hide': True},
                {'title': "В начало", 'hide': True},
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


def add_user_db(name, user_id):
    requests.post(URL + '/api/v1/alice_users', json={
        "name": name, "id_user": user_id
    }).json()


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5057, debug=True)
