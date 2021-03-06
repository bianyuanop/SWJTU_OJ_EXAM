import json
import datetime
from flask import current_app 
from sqlalchemy import Column, DateTime, String, Integer, ForeignKey, func, create_engine
from sqlalchemy.orm import relationship, backref, sessionmaker
from sqlalchemy.ext.declarative import declarative_base, DeclarativeMeta

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
    class_id      = Column(Integer, ForeignKey('classes.id'))
    email         = Column(String(256))
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
    # there is a conversion from js request json to python object to sql object
    start_t       = Column(DateTime, default=func.now())
    end_t         = Column(DateTime, default=func.now())
    # This column is set for a config file of a exam
    # The configure here is generated by func -> question_set_gen 
    # not equal to admin.py mentioned 
    info          = Column(String(2048))
    describe      = Column(String(1024))

class Grades(Base):

    __tablename__ = 'grades'
    id            = Column(Integer, primary_key=True, autoincrement=True)
    exam_id       = Column(Integer, ForeignKey("exams.id"))
    user_id       = Column(Integer, ForeignKey('users.id'))
    total_score   = Column(Integer)
    # store json or yaml string that contains multiple types of the score
    sub_score     = Column(String(2048))
    
class Classes(Base):

    __tablename__ = 'classes'
    id = Column(Integer, primary_key=True, autoincrement=True)
    class_name = Column(String(256), nullable=False)
    join_code = Column(String(1024), nullable=False)
    describe = Column(String(1024))

class Admins(Base):

    __tablename__ = 'admins'
    id = Column(Integer, primary_key=True, autoincrement=True)
    admin_name = Column(String(256), nullable=False)
    password = Column(String(256), nullable=False)

class Events(Base):
    
    __tablename__ = 'events'
    id = Column(Integer, primary_key=True, autoincrement=True)
    related_class_id = Column(Integer, ForeignKey('classes.id'))
    event_type = Column(Integer, ForeignKey('event_types.id'))
    event_title = Column(String(256), nullable=False)
    event_msg = Column(String(2048))


class EventTypes(Base):

    __tablename__ = 'event_types'
    id = Column(Integer, primary_key=True, autoincrement=True)
    type_name = Column(String(256), nullable=False)
    describe = Column(String(2048))

class Questions(Base):
    '''
    basic question type:
        - select
        - fill
        - fix
        - coding
    '''
    __tablename__ = 'questions'
    id = Column(Integer, primary_key=True, autoincrement=True)
    question_type = Column(String(64))
    content = Column(String(4096)) 
    answer = Column(String(1024))


# gen question here and insert to exam
def question_set_gen(config):
    pass

# Serialize cls
# how to use
#c = YourAlchemyClass()
#print( json.dumps(c, cls=AlchemyEncoder) )

class AlchemyEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj.__class__, DeclarativeMeta):
            # an SQLAlchemy class
            fields = {}
            for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata']:
                data = obj.__getattribute__(field)
                try:
                    # More data convert place here
                    if type(data) is datetime.datetime:
                        data = str(data)
                    else:
                        # this will fail on non-encodable values, like other classes
                        data = json.dumps(data) 

                    fields[field] = data
                except TypeError:
                    fields[field] = None
            # a json-encodable dict
            return fields

        return json.JSONEncoder.default(self, obj)

