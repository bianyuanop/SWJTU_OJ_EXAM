from flask import Flask
from flask_restful import Resource, Api, reqparse

app = Flask(__name__)
api = Api(app)
parsers = {
        "User": reqparse.RequestParser()
            .add_argument('password', type=str, help='password must be string'),
        "Users": reqparse.RequestParser()
            .add_argument('username', type=str, help='username must be string')
            .add_argument('password', type=str, help='password must be string')
}
users = {}


class User(Resource):
    def __init__(self):
        self.__name__ = "User"


    def get(self, u_id):
        """
        @api {get} /user/:username Request User infomation
        @apiName GetUser
        @apiGroup User

        @apiParam {String} username Users' name
        @apiSuccess {String} username 
        @apiSuccess {String} password 
        """
        return {"username": u_id, "password": users.get(u_id)}

    def delete(self, u_id):
        """
        @api {delete} /user/:username Delete one user
        @apiName DelUser
        @apiGroup User

        @apiParam {String} username Users' name
        @apiSuccess {String} i_status Instruction status 
        """
        if users.get(u_id):
            users.pop(u_id)
            return {"i_status": "1"}
        else:
            return {"i_status": "0"}

    def put(self, u_id):
        """
        @api {put} /user/:username Update one user's password
        @apiName UpdatePassword
        @apiGroup User

        @apiParam {String} username Users' name
        @apiSuccess {String} i_status Instruction status 
        """
        args = parsers[self.__name__].parse_args()
        pwd = args["password"]
        if users.get(u_id):
            users[u_id] = pwd
            return {"i_status": "1"}
        else:
            return {"i_status": "0"}


class Users(Resource):
    
    def __init__(self):
        self.__name__ = "Users"

    def get(self):
        """
        @api {get} /users Get all users infomation
        @apiName GetUsers
        @apiGroup User

        @apiSuccess {String} i_status Instruction status 
        """
        return users

    def post(self):
        """
        @api {get} /users Get all users infomation
        @apiName GetUsers
        @apiGroup User

        @apiParam {String} username Users' name
        @apiParam {String} password Password

        @apiSuccess {String} i_status Instruction status 
        """
        args = parsers[self.__name__].parse_args()
        username = args['username']
        password = args['password']
        users[username] = password

        return {"i_status": "1"}


api.add_resource(Users, '/users')
api.add_resource(User, '/user/<u_id>')

if __name__ == '__main__':
    app.run(debug=True)
