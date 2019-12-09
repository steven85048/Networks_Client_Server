from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from db_model import Base, ClientAccount, Messages, Subscriptions

engine = create_engine('postgresql+psycopg2://root:12345@3.136.156.128/networks-messaging-server')
connection = engine.connect()

Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)

session = DBSession()

new_account = ClientAccount(username='ac1', password='pass1')
session.add(new_account)
session.commit()