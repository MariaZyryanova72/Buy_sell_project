from flask import jsonify
from flask_restful import reqparse, abort, Resource
from data import db_session
from data.categories import Category

parser = reqparse.RequestParser()
parser.add_argument('name', required=True, type=str)


def abort_if_category_not_found(category_id):
    session = db_session.create_session()
    category = session.query(Category).get(category_id)
    if not category:
        abort(404, message=f"Category {category_id} not found")


class CategoryUsersResource(Resource):
    def get(self, category_id):
        abort_if_category_not_found(category_id)
        session = db_session.create_session()
        category = session.query(Category).get(category_id)
        return jsonify({'category': category.to_dict(
            only=('name',))})

    def delete(self, category_id):
        abort_if_category_not_found(category_id)
        session = db_session.create_session()
        category = session.query(Category).get(category_id)
        session.delete(category)
        session.commit()
        return jsonify({'success': 'OK'})


class CategoryUsersListResource(Resource):
    def get(self):
        session = db_session.create_session()
        categories = session.query(Category).all()
        return jsonify({'categories': [item.to_dict(
            only=("name",)) for item in categories]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        categories = Category(
            name=args['name'],
        )
        session.add(categories)
        session.commit()
        return jsonify({'success': 'OK'})
