import datetime
import sqlalchemy
from my_pypi.data.modelbase import SqlAlchemyBase


class Audit(SqlAlchemyBase):
    __tablename__ = 'auditing'

    id: str = sqlalchemy.Column(sqlalchemy.String, primary_key=True)
    created_date: datetime.datetime = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now, index=True)
    description: str = sqlalchemy.Column(sqlalchemy.String)
