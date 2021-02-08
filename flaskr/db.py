from sqlalchemy import Column, DateTime, String, Integer, ForeignKey, func
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

def init_db():
    engine = create_engine("mysql+pymysql://chan:diy.2002@localhost/test_db")

    session = sessionmaker()
    session.configure(bind=engine)

    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

def get_session():
    engine = create_engine("mysql+pymysql://chan:diy.2002@localhost/test_db")
    session = sessionmaker()
    session.configure(engine)

    return session


class Majors(Base):
    __tablename__ = 'majors'
    id            = Column(Integer, primary_key=True)
    major_name    = Column(String(200))


class Users(Base):
    __tablename__ = 'users'
    id            = Column(Integer, primary_key=True)
    stu_id        = Column(Integer, primary_key=True)
    name          = Column(String(64))
    real_name     = Column(String(20))
    grade         = Column(String(20))
    major_id      = Column(Integer, ForeignKey('majors.id'))
    register_at   = Column(DateTime, default=func.now())
    
class Exams(Base):
    __tablename__ = 'exams'
    id            = Column(Integer, primary_key=True)
    name          = Column(String(200))
    start_t       = Column(DateTime, default=func.now())
    end_t         = Column(DateTime, default=func.now())
    describe      = Column(String(500))

class Grades(Base):
    __tablename__ = 'grades'
    id            = Column(Integer, primary_key=True)
    exam_id       = Column(Integer, ForeignKey("exams.id"))
    user_id       = Column(Integer, ForeignKey('users.id'))
    total_score   = Column(Integer)
    # store json or yaml string that contains multiple types of the score
    sub_score     = Column(String(1000))
    
