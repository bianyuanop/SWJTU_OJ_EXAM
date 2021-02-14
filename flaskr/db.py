from flask import current_app 

from sqlalchemy import Column, DateTime, String, Integer, ForeignKey, func
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


def get_connection_str():
    engine_connection_str = current_app.config["DB_URI"] + current_app.config["DB_ADMIN"] + ':' + current_app.config["DB_PASS"] + '@'  + current_app.config["DB_ADDR"] + '/' + current_app.config["DB_NAME"] 
    return engine_connection_str

def init_db(connection_str=None):
    if connection_str:
        engine = create_engine(connection_str)
    else:
        engine = create_engine("mysql+pymysql://chan:diy.2002@localhost/test_db")

    session = sessionmaker()
    session.configure(bind=engine)

    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

def get_session_factory(connection_str=None):
    if connection_str:
        engine = create_engine(connection_str)
    else:
        engine = create_engine("mysql+pymysql://chan:diy.2002@localhost/test_db")

    session = sessionmaker()
    session.configure(bind=engine)

    return session


class Majors(Base):
    __tablename__ = 'majors'
    id            = Column(Integer, primary_key=True, autoincrement=True)
    major_name    = Column(String(256))


class Users(Base):
    __tablename__ = 'users'
    id            = Column(Integer, primary_key=True, autoincrement=True)
    stu_id        = Column(Integer, primary_key=True, unique=True)
    password      = Column(String(256))
    name          = Column(String(64), unique=True, nullable=False)
    real_name     = Column(String(32))
    grade         = Column(String(128))
    major_id      = Column(Integer, ForeignKey('majors.id'))
    register_at   = Column(DateTime, default=func.now())
    
class Exams(Base):
    __tablename__ = 'exams'
    id            = Column(Integer, primary_key=True, autoincrement=True)
    name          = Column(String(256))
    start_t       = Column(DateTime, default=func.now())
    end_t         = Column(DateTime, default=func.now())
    describe      = Column(String(1024))

class Grades(Base):
    __tablename__ = 'grades'
    id            = Column(Integer, primary_key=True, autoincrement=True)
    exam_id       = Column(Integer, ForeignKey("exams.id"))
    user_id       = Column(Integer, ForeignKey('users.id'))
    total_score   = Column(Integer)
    # store json or yaml string that contains multiple types of the score
    sub_score     = Column(String(2048))
    

