from flask import Flask, Blueprint, session
from flask_restful import Api, Resource

bp = Blueprint("exam", __name__)
api = Api(bp)


#The get method is about to return a problem set of a exam
class Exam(Resource):

    def get(self):
        pass

#return a list of exams
class Exams(Resource):
    
    def get(self):
        pass
