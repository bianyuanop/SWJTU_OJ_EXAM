import random, string
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, func
import db
# run the script beyond tests folder

Session = sessionmaker()
engine = create_engine('mysql+pymysql://chan:diy.2002@localhost/test_db')
Session.configure(bind=engine)


def gen_random_string():
    ascii_chars = string.ascii_letters
    return ''.join( random.choice(ascii_chars) for i in range( random.randint(10,15) ) )

    

q_types = [
    'select',
    'coding',
    'fix',
    'fill'
]

each_amount = 100

try:
    s = Session()
    for q_type in q_types:
        quess = []
        for i in range(each_amount):
            q = db.Questions(
                question_type = q_type,
                content = gen_random_string(),
                answer = gen_random_string()
            )
            quess.append(q)
        
        s.add_all(quess)
        quess = []

    s.commit()
except Exception as e:
    s.rollback()
    print(e)
finally:
    s.close()
