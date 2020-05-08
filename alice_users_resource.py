from flask import jsonify
from flask_restful import reqparse, abort, Resource
from data import db_session
from data.alice_users import AliceUser

parser = reqparse.RequestParser()
parser.add_argument('name', required=True, type=str)
parser.add_argument('id_user', required=True, type=str)


def abort_if_user_not_found(user_id):
    session = db_session.create_session()
    user = session.query(AliceUser).get(user_id)
    if not user:
        abort(404, message=f"User {user_id} not found")


class AliceUsersResource(Resource):
    def get(self, user_id):
        abort_if_user_not_found(user_id)
        session = db_session.create_session()
        user = session.query(AliceUser).get(user_id)
        return jsonify({'users': user.to_dict(
            only=('name', 'id_user'))})

    def delete(self, user_id):
        abort_if_user_not_found(user_id)
        session = db_session.create_session()
        user = session.query(AliceUser).get(user_id)
        session.delete(user)
        session.commit()
        return jsonify({'success': 'OK'})


class AliceUsersListResource(Resource):
    def get(self):
        session = db_session.create_session()
        users = session.query(AliceUser).all()
        return jsonify({'user': [item.to_dict(
            only=('name', 'id_user')) for item in users]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        users = AliceUser(
            name=args['name'],
            id_user=args['id_user'],
        )
        session.add(users)
        session.commit()
        return jsonify({'success': 'OK'})
