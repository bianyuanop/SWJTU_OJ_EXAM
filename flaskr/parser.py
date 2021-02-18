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

