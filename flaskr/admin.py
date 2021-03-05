import jwt
import json
from flask import Flask, Blueprint, session, g, current_app
from flask_restful import Api, Resource
from .parser import user_query_parser, admin_login_parser, exam_charge_parser
from . import db, func
from .log import Logger

l = Logger(location='ADMIN')

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
        if g.get('admin'):
            msg = {
                    "i_status": 0,
                    "err_code": 5,
                    "msg": "Already login."
                    }

        args = admin_login_parser.parse_args(strict=True)
        admin_name = args.get('admin_name') or ""
        password = args.get('password') or ""

        if not (admin_name and password):
            msg = {
                    "i_status": 0,
                    "err_code": 0,
                    "msg": "admin username or password not provided when admin"
                    }
            return msg
        
        safe = check_spell(admin_name) and check_spell(password)
        if not safe:
            msg = {
                    "i_status": 0,
                    "err_code": 7,
                    "msg": "password or username not format well when."
                    }
            return msg
        
        #TODO: say auth.py, the same
        try:
            s = g.Session()
            
        except:
            #TODO: add a log here
            pass
        finally:
            s.close()


                 

#Users charge
#Users charge based on User charge
#TODO: use sqlalchemy query delete, add, update, get
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
    
# Same with UserCharge
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
#config_example = {
#        'title': 'aTitle',
#        'start_time': "a string with time format contains %Y/%m/%d %H:%M:%S",
#        'duration': "%H:%M:%S",
##        # the problem setting must be format like this and convert it to string
#        'problem_set_config': [
#            {
#                'type': 'select',
#                'number': 20,
#                'percentage_tatol': 0.4
#                },
#            {
#                'type': 'fill',
#                'number': 10,
#                'percentage_tatol': 0.2
#                },
#            {
#                'type': 'fix',
#                'number': 10,
#                'percentage_tatol': 0.2
#                },
#            {
#                'type': 'coding',
#                'number': 2,
#                'percentage_tatol': 0.2
#                },
#            ]
#        }
# Need request test
class ExamCharge(Resource):
    def post(self):
        args = exam_charge_parser.parse_args(strict=True)
        err = False
        try:
            l.debug( args.get('problem_set_config')  + str(type(args.get('problem_set_config'))))
            config = {
                'start_time': args.get('start_time'),
                'duration': args.get('duration'),
                'problem_set_config': json.loads(args.get('problem_set_config'))
            }
            exam_configure = func.question_set_config_gen(config)
        except Exception as e:
            l.error(str(e))
            err = True
        
        if err:
            msg = {
                    "i_status": 0,
                    "err_code": 8,
                    "msg": "Configure format err."
                    }
            return msg
        

        s = g.Session()
        try:
            exam = db.Exams(
                name     = args.get('title'),
                start_t  = exam_configure.get('start_time'),
                end_t    = exam_configure.get('end_time'),
                info     = str(exam_configure),
                describe = args.get('desc')
            ) 
            s.add(exam)
            s.commit()
        except Exception as e:
            err = True
            l.error(e)
        finally:
            s.close()

        if err:
            msg = {
                    "i_status": 0,
                    "err_code": 999,
                    "msg": "General Error, no idea how would it happend."
                    }
            return msg

        msg = {
                "i_status": 1,
                "err_code": -1,
                "msg": ""
                }
        return msg



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

api.add_resource(ExamCharge, '/admin/exam-charge')

