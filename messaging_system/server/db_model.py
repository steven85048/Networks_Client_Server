from sqlalchemy import create_engine, ForeignKey, Column, Integer, String, JSON, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import datetime

Base = declarative_base()

class ClientAccount(Base):
    __tablename__ = 'client_account'

    username = Column(String(250), primary_key=True)
    password = Column(String(250), nullable=False)
    token = Column(JSON)

class Messages(Base):
    __tablename__ = 'messages'

    id = Column(Integer, primary_key=True)

    message = Column(String(250))
    account = relationship(ClientAccount)
    account_name = Column(String(250), ForeignKey('client_account.username'))
    post_time = Column(Date, default=datetime.datetime.now)

class Subscriptions(Base):
    __tablename__ = 'subscriptions'

    id = Column(Integer, primary_key=True)

    subscriber_username = Column(String(250), ForeignKey('client_account.username'), nullable=False)
    subscription_username = Column(String(250), ForeignKey('client_account.username'), nullable=False)

    subscription = relationship(ClientAccount, foreign_keys=[subscriber_username])
    subscriber = relationship(ClientAccount, foreign_keys=[subscription_username])

def create_all():
    # psql -h 3.136.156.128 -p 5432 -U root networks-messaging-server
    # to connect to dev database
    engine = create_engine('postgresql+psycopg2://root:12345@3.136.156.128/networks-messaging-server')
    connection = engine.connect()

    Base.metadata.create_all(engine)

def drop_all():
    engine = create_engine('postgresql+psycopg2://root:12345@3.136.156.128/networks-messaging-server')
    connection = engine.connect()

    Base.metadata.drop_all(engine)

if __name__ == '__main__':
    create_all()