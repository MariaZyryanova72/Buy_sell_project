import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin
from .db_session import SqlAlchemyBase


class Advertising(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'advertisings'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String)
    image = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    vk = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    instagram = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    site = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    telephone = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    price = sqlalchemy.Column(sqlalchemy.String)
    text = sqlalchemy.Column(sqlalchemy.Text)
    create_date = sqlalchemy.Column(sqlalchemy.DateTime)
    id_alice_user = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    id_user = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    id_category = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("categories.id"))
    categories = orm.relation("Category")
