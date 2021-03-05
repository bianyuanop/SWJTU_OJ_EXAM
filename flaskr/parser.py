from flask_restful import reqparse

# Authentication parsers
login_parser = reqparse.RequestParser()
login_parser.add_argument('username', type=str)
login_parser.add_argument('password', type=str)

register_parser = reqparse.RequestParser()
register_parser.add_argument('username', type=str)
register_parser.add_argument('password', type=str)
register_parser.add_argument('student_id', type=str)


# Admin parsers
user_query_parser = reqparse.RequestParser()
user_query_parser.add_argument('u_id', type=int)
user_query_parser.add_argument('username', type=str)
user_query_parser.add_argument('student_id', type=int)

## admin login parser
admin_login_parser = reqparse.RequestParser()
admin_login_parser.add_argument('admin_name', type=str)
admin_login_parser.add_argument('password', type=int)

#Exam Charge parsers 
## Exam charge parser - post
exam_charge_parser = reqparse.RequestParser()
exam_charge_parser.add_argument('start_time', type=str)
exam_charge_parser.add_argument('title', type=str)
exam_charge_parser.add_argument('desc', type=str)
exam_charge_parser.add_argument('duration', type=str)
exam_charge_parser.add_argument('problem_set_config', type=str)

