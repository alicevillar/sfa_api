from flask import Flask
from flask_restplus import Resource, Api
from controllers.picture_controller import *
from flask import Flask, request
from flask_restplus import Api

class API():
    def __init__(self):
        defining_authorizations = {'apikey':  {'type': 'apiKey','in': 'header', 'name': 'X-API-KEY'}}
        self.app = Flask(__name__)
        self.app.secret_key = 'super secret string' # gerenciamento de sessão para guardar info e poder usar p/ o login
        self.api = Api(self.app,version='1.0.0',title=str('Space Fan Art (SFA)'),
                       description='This API, called SFA (Space Fan Art), is an API created with Flask REST-Plus following the best practices proven to secure a REST-API and showcasing the OWASP Top Ten Proactive Controls. Users have to register to get an authentication key, which allows them to download and upload images from NASA',
                       doc='/docs',authorizations=defining_authorizations)#docs é a rota q está direcionando para a API do swagger

    def run(self, ):
        self.app.run(debug=True,port=5000)

# variable sfa_app ==> objet of the class API
sfa_app = API()


