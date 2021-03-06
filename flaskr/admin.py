import jwt
import json
from flask import Flask, Blueprint, session, g, current_app
from flask_restful import Api, Resource
from .parser import user_query_parser, admin_login_parser, exam_charge_parser, exam_charge_parser_get, exam_charge_parser_put, exam_charge_parser_delete, exams_charge_delete
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
    """
    @api {post} /api/exam/add ExamAdd
    @apiName ExamPost
    @apiGroup Admin

    @apiParam {String} start_time Exam start time
    @apiParam {String} title Exam title.
    @apiParam {String} desc Exam describe.
    @apiParam {String} duration Exam duration.
    @apiParam {String} problem_set_config Problem set config, details can be seen in the doc.
    
    @apiSuccess {Number} i_status Instruction success status.
    @apiSuccess {Number} err_code Error code.
    @apiSuccess {String} msg Message.
    @apiVersion 0.0.1
    """
    def post(self):
        args = exam_charge_parser.parse_args(strict=True)
        err = False
        try:
            l.debug(str(args))
            config = {
                'start_time': args.get('start_time'),
                'duration': args.get('duration'),
                'problem_set_config': json.loads(args.get('problem_set_config'))
            }
            exam_configure = func.question_set_config_gen(config)
        except Exception as e:
            l.error(str(e))
            err = True
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
        args = exam_charge_parser_get.parse_args(strict=True)
        exam_id = args.get('exam_id')
        s = g.Session()
        try:
            exam = s.query(db.Exams).filter(db.Exams.id == exam_id).first()
            msg = {
                    "i_status": 1,
                    "err_code": -1,
                    "msg": "",
                    # The AlchemyEncode Serilizer has no feature of decoding datetime
                    "deliver": json.dumps(exam, cls=db.AlchemyEncoder)
                    }
        except Exception as e:
            l.error(str(e)) 
            msg = {
                    "i_status": 0,
                    "err_code": 998,
                    "msg": "Query error.",
                    }
        finally:
            s.close()


        return msg
        

    def delete(self):
        args = exam_charge_parser_delete.parse_args(strict=True)
        exam_id = args.get('exam_id')
        s = g.Session()
        try:
            exam = s.query(db.Exams).filter(db.Exams.id == exam_id).delete()
            msg = {
                    "i_status": 1,
                    "err_code": -1,
                    "msg": "",
                    }
        except Exception as e:
            l.error(str(e))
            msg = {
                    "i_status": 0,
                    "err_code": 998,
                    "msg": "Query error.",
                    }
        finally:
            s.close()

        return msg


    # configuration change
    #TODO: maybe later, not so emergency now
    def put(self):
        pass

class ExamsCharge(Resource):
    
    """
    @api {get} /api/admin/exams-charge Get exams
    @apiName Get-exams
    @apiGroup Admin

    @apiSuccess {Number} i_status Instruction success status.
    @apiSuccess {Number} err_code Error code.
    @apiSuccess {String} msg Message.
    @apiVersion 0.0.1
    """
    def get(self):
        s = g.Session()
        try:
            exams = s.query(db.Exams).all() 
            msg = {
                    "i_status": 1,
                    "err_code": -1,
                    "msg": "",
                    "deliver": json.dumps(exams, cls=db.AlchemyEncoder)
                    }
        except Exception as e:
            l.error(str(e))
            msg = {
                    "i_status": 0,
                    "err_code": 998,
                    "msg": "Query error.",
                    }
        finally:
            s.close()

        return msg

    """
    @api {delete} /api/admin/exams-charge Delete exams
    @apiName Delete-exams
    @apiGroup Admin

    @apiParam {String} exam_ids Exam ids like "1,2,3,4" split by ','

    @apiSuccess {Number} i_status Instruction success status.
    @apiSuccess {Number} err_code Error code.
    @apiSuccess {String} msg Message.
    @apiVersion 0.0.1
    """
    def delete(self):
        args = exams_charge_delete.parse_args(strict=True)
        ids = [int(id) for id in args.get('exam_ids').split(',')]
        s = g.Session()
        for id in ids:
            try:
                s.query(db.Exams).filter(db.Exams.id == id).delete()
            except Exception as e:
                l.error("DELETE {0} failed, ".format(id), str(e))
            
        try:
            s.commit()
            s.close()
        except:
            pass

        msg = {
                "i_status": 1,
                "err_code": -1,
                "msg": "",
                }
        return msg

api.add_resource(ExamCharge, '/admin/exam-charge')
api.add_resource(ExamsCharge, '/admin/exams-charge')

