from flask import Flask, request
import logging

from data import db_session
from alice.main import dialog_alice

logging.basicConfig(level=logging.INFO)
sessionStorage = {}

app = Flask(__name__)
app.config['SECRET_KEY'] = 'bfhdjwiskoldjEFE4GUJFTYGGG5G5G65H6G565F3222JGTHGRFDJSKE;ROJELAGTRH4TF'


def main():
    db_session.global_init("db/buy_sell_db.sqlite")
    app.run(port=5055)


@app.route('/alice', methods=['POST'])
def alice():
    return dialog_alice(request)


if __name__ == '__main__':
    main()
