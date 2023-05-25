import sqlalchemy as sa
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    username = sa.Column(sa.String, unique=True)
    uuid = sa.Column(sa.UUID(as_uuid=True), unique=True)


class Record(Base):
    __tablename__ = 'record'

    uuid = sa.Column(sa.UUID(as_uuid=True), unique=True, primary_key=True)
    user_id = sa.Column(sa.ForeignKey('user.id'))
    path = sa.Column(sa.String)
