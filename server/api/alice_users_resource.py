from flask import jsonify
from flask_restful import reqparse, abort, Resource
from server.data import db_session
from server.data.alice_users import AliceUser

parser = reqparse.RequestParser()
parser.add_argument('name', required=True, type=str)
parser.add_argument('id_user', required=True, type=str)


class AliceUsersResource(Resource):
    def get(self, user_id):
        print(user_id)
        session = db_session.create_session()
        user = session.query(AliceUser).filter(AliceUser.id_user == user_id).first()
        if not user:
            abort(404, error=f"User {user_id} not found")
        return jsonify({'user': user.to_dict(
            only=('name', 'id_user'))})

    def delete(self, user_id):
        session = db_session.create_session()
        user = session.query(AliceUser).filter(AliceUser.id_user == user_id).first()
        if not user:
            abort(404, error=f"User {user_id} not found")
        session.delete(user)
        session.commit()
        return jsonify({'success': 'OK'})


class AliceUsersListResource(Resource):
    def get(self):
        session = db_session.create_session()
        users = session.query(AliceUser).all()
        return jsonify({'users': [item.to_dict(
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
