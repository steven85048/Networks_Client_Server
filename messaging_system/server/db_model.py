from sqlalchemy import create_engine, ForeignKey, Column, Integer, String, JSON, DateTime
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

    to_account_username = Column(String(250), ForeignKey('client_account.username'))
    from_account_username = Column(String(250), ForeignKey('client_account.username'))

    to_account = relationship(ClientAccount, foreign_keys=[to_account_username])
    from_account = relationship(ClientAccount, foreign_keys=[from_account_username])

    post_time = Column(DateTime, default=datetime.datetime.utcnow)

class Subscriptions(Base):
    __tablename__ = 'subscriptions'

    id = Column(Integer, primary_key=True)

    subscriber_username = Column(String(250), ForeignKey('client_account.username'), nullable=False)
    subscription_username = Column(String(250), ForeignKey('client_account.username'), nullable=False)

    subscription = relationship(ClientAccount, foreign_keys=[subscriber_username])
    subscriber = relationship(ClientAccount, foreign_keys=[subscription_username])

def create_all(engine):
    # psql -h 3.136.156.128 -p 5432 -U root networks-messaging-server
    # to connect to dev database
    Base.metadata.create_all(engine)

def drop_all(engine):
    Base.metadata.drop_all(engine)

if __name__ == '__main__':
    engine = create_engine('postgresql+psycopg2://root:12345@3.136.156.128/networks-messaging-server')
    connection = engine.connect()

    create_all(engine)