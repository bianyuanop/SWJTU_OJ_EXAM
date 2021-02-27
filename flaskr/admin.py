import jwt
from flask import Flask, Blueprint, session, g
from flask_restful import Api, Resource
from .parser import user_query_parser, admin_login_parser
from . import db

bp = Blueprint("admin", __name__)
api = Api(bp)

default_admin = "root"
default_password = "alongpassword"


class AdminAuth(Resource):
    
    """
    @api {post} /api/amdin/auth/login Login
    @apiName Login
    @apiGroup Admin

    @apiParam {String} admin name
    @apiParam {String} admin password

    @apiSuccess {Number} i_status Instruction success status.
    @apiSuccess {Number} err_code Error code.
    @apiSuccess {String} msg Message.
    @apiVersion 0.0.0
    """
    def post(self):
        if g.admin:
            msg = {
                    "i_status": 0,
                    "err_code": 5,
                    "msg": "Already login."
                    }

        args = admin_login_parser.parse_args(strict=True)
        admin_name = args.get('admin_name') or ""
        password = args.get('password') or ""



                 

class UserCharge(Resource):

    def post(self):
        pass
    
    def delete(self):
        pass

    def get(self):
        pass

class UsersCharge(Resource):

    def get(self):
        pass

    def delete(self):
        pass
    
class AdminCharge(Resource):

    def post(self):
        pass

    def delete(self):
        pass

    def get(self):
        pass

# Event receive when user flashing
class EventCharge(Resource):

    def post(self):
        pass
    
    def get(self):
        pass

    def delete(self):
        pass

# Some infomation must be set for exam
# The configure can be format -json or -yaml
# - exam start time
# - exam duration
# - point weight/percentage of each problem
# a Example format
config_example = {
        'start_time': "a string with time format contains %Y/%m/%d %H:%M:%S",
        'duration': "%Y/%m/%d %H:%M:%S",
        'problem_set_config': [
            {
                'type': 'select',
                'number': 20,
                'percentage_tatol': 0.4
                },
            {
                'type': 'fill',
                'number': 10,
                'percentage_tatol': 0.2
                },
            {
                'type': 'fix',
                'number': 10,
                'percentage_tatol': 0.2
                },
            {
                'type': 'coding',
                'number': 2,
                'percentage_tatol': 0.2
                },
            ]
        }
# TODO: need a more detailed configure of a exam
class ExamCharge(Resource):
    
    def post(self):
        pass

    def get(self):
        pass

    def delete(self):
        pass

    # configuration change
    def put(self):
        pass

class ExamsCharge(Resource):
    
    def get(self):
        pass
    
    def delete(self):
        pass
