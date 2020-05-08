from flask import jsonify
from flask_restful import reqparse, abort, Resource
from data import db_session
from data.advertisings import Advertising

parser = reqparse.RequestParser()
parser.add_argument('title', required=True, type=str)
parser.add_argument('image', required=False, type=str)
parser.add_argument('vk', required=False, type=str)
parser.add_argument('instagram', required=False, type=str)
parser.add_argument('site', required=False, type=str)
parser.add_argument('telephone', required=False, type=str)
parser.add_argument('price', required=True, type=str)
parser.add_argument('text', required=True, type=str)
parser.add_argument('id_alice_user', required=False, type=str)
parser.add_argument('id_user', required=False, type=int)
parser.add_argument('id_category', required=True, type=int)


def abort_if_advertising_not_found(ad_id):
    session = db_session.create_session()
    advertising = session.query(Advertising).get(ad_id)
    if not advertising:
        abort(404, message=f"Advertising {ad_id} not found")


class AdvertisingUsersResource(Resource):
    def get(self, ad_id):
        abort_if_advertising_not_found(ad_id)
        session = db_session.create_session()
        advertising = session.query(Advertising).get(ad_id)
        return jsonify({'advertising': advertising.to_dict(
            only=('title', 'image', 'vk', 'instagram', 'site', 'telephone', 'price',
                  'text', 'id_alice_user', 'id_user', 'id_category'))})

    def delete(self, ad_id):
        abort_if_advertising_not_found(ad_id)
        session = db_session.create_session()
        advertising = session.query(Advertising).get(ad_id)
        session.delete(advertising)
        session.commit()
        return jsonify({'success': 'OK'})


class AdvertisingUsersListResource(Resource):
    def get(self):
        session = db_session.create_session()
        advertisings = session.query(Advertising).all()
        return jsonify({'advertisings': [item.to_dict(
            only=('title', 'image', 'vk', 'instagram', 'site', 'telephone', 'price',
                  'text', 'id_alice_user', 'id_user', 'id_category')) for item in advertisings]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        advertisings = Advertising(
            title=args['title'],
            image=args['image'],
            vk=args['vk'],
            instagram=args['instagram'],
            site=args['site'],
            telephone=args['telephone'],
            price=args['price'],
            text=args['text'],
            id_alice_user=args['id_alice_user'],
            id_user=args['id_user'],
            id_category=args['id_category'],

        )
        session.add(advertisings)
        session.commit()
        return jsonify({'success': 'OK'})
