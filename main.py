from flask import Flask, request
import logging
import json

from data import db_session
from data.users import User


logging.basicConfig(level=logging.INFO)
sessionStorage = {}

app = Flask(__name__)
app.config['SECRET_KEY'] = 'bfhdjwiskoldjEFE4GUJFTYGGG5G5G65H6G565F3222JGTHGRFDJSKE;ROJELAGTRH4TF'


def main():
    db_session.global_init("db/buy_sell_db.sqlite")
    app.run(port=5055)


@app.route('/alice', methods=['POST'])
def alice():
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
        session = db_session.create_session()
        user = session.query(User).filter(User.id_user == user_id).first()
        if user:
            res['response']['text'] = f'Привет, { user.name }!'
            sessionStorage[user_id] = {
                'settings': '',
                'first_name': user.name
            }
            return
        else:
            res['response']['text'] = 'Привет! Назови свое имя!'
            sessionStorage[user_id] = {
                'settings': '',
                'first_name': None
            }
            return

    if sessionStorage[user_id]['first_name'] is None:
        first_name = get_first_name(req)
        if first_name is None:
            res['response']['text'] = \
                'Не расслышала имя. Повтори, пожалуйста!'
        else:
            sessionStorage[user_id]['first_name'] = first_name[0].upper() + first_name[1:]
            add_user_db(sessionStorage[user_id]['first_name'], user_id)
            res['response']['text'] = f"Приятно познакомиться, { sessionStorage[user_id]['first_name'] }!"


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


if __name__ == '__main__':
    main()
