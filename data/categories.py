import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin
from .db_session import SqlAlchemyBase


class Category(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'categories'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String)
    id_parent_category = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    end_category = sqlalchemy.Column(sqlalchemy.Boolean)
    advertisings = orm.relation("Advertising", back_populates='categories')
