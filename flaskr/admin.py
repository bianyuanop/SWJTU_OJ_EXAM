from flask import Flask, Blueprint, session, g
from flask_restful import Api, Resource
from .parser import user_query_parser
from . import db

bp = Blueprint("admin", __name__)
api = Api(bp)


default_admin = "root"
default_password = "alongpassword"

class UserCharge(Resource):

    def post(self):
        pass
    
    def delete(self):
        pass

    def get(self):
        pass

    
class AdminCharge(Resource):

    def post(self):
        pass

    def delete(self):
        pass

    def get(self):
        pass

class EventCharge(Resource):

    def post(self):
        pass
    
    def get(self):
        pass

    def delete(self):
        pass

class ExamCharge(Resource):
    
    def post(self):
        pass

    def get(self):
        pass

    def delete(self):
        pass
