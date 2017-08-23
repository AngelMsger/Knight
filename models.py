from sqlalchemy import Column, Integer, String, DATETIME
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from settings import DB_URI

engine = create_engine(DB_URI, encoding='utf8')

BaseModel = declarative_base(bind=engine)
DBSession = sessionmaker(bind=engine)

session = DBSession()


class ChatLog(BaseModel):
    __tablename__ = 'chat_logs'

    id = Column(Integer, primary_key=True)
    MsgId = Column(String)
    FromUserName = Column(String, nullable=False)
    Content = Column(String)
    CreateTime = Column(DATETIME, nullable=False)


class KeyWordsCache(BaseModel):
    __tablename__ = 'key_words_caches'

    id = Column(Integer, primary_key=True)
    FromUserName = Column(String, nullable=False)
    Content = Column(String)
    CreateTime = Column(DATETIME, nullable=False)


BaseModel.metadata.create_all(engine)
