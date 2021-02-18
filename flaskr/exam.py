from flask import Flask, Blueprint, session
from flask_restful import Api, Resource

bp = Blueprint("exam", __name__)
api = Api(bp)

class Exam(Resource):
    pass

class Exams(Resource):
    pass
