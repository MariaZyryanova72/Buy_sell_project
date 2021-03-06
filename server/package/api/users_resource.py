from flask import jsonify
from flask_restful import reqparse, abort, Resource
from package.data import db_session
from package.data.users import User

parser = reqparse.RequestParser()
parser.add_argument('name', required=True, type=str)
parser.add_argument('city', required=False, type=str)
parser.add_argument('address', required=False, type=str)
parser.add_argument('email', required=True, type=str)


def abort_if_user_not_found(user_id):
    session = db_session.create_session()
    user = session.query(User).get(user_id)
    if not user:
        abort(404, message=f"User {user_id} not found")


class UsersResource(Resource):
    def get(self, user_id):
        abort_if_user_not_found(user_id)
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        return jsonify({'users': user.to_dict(
            only=('name', 'city', 'address', 'email'))})

    def delete(self, user_id):
        abort_if_user_not_found(user_id)
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        session.delete(user)
        session.commit()
        return jsonify({'success': 'OK'})


class UsersListResource(Resource):
    def get(self):
        session = db_session.create_session()
        users = session.query(User).all()
        return jsonify({'users': [item.to_dict(
            only=('name', 'city', 'address', 'email')) for item in users]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        users = User(
            name=args['name'],
            city=args['city'],
            address=args['address'],
            email=args['email'],
        )
        session.add(users)
        session.commit()
        return jsonify({'success': 'OK'})
