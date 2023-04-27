import sqlalchemy
from .db_session import SqlAlchemyBase


class AddProduct(SqlAlchemyBase):
    __tablename__ = 'add_product'
    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)