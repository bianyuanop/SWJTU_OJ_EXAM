from flask import Flask, Blueprint, session
from flask_restful import Api, Resource

bp = Blueprint("event",__name__)
api = Api(bp)

