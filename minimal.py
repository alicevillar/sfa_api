from flask import Flask
from flask_restplus import Resource, Api
from controllers.picture_controller import *
from flask import Flask, request
from flask_restplus import Api


class API():
    def __init__(self):
        # Metodo api contém tb o parametro contido na variável authorizations - > A Swagger Authorizations declaration as dictionary
        defining_authorizations = {'apikey':  {'type': 'apiKey','in': 'header', 'name': 'X-API-KEY'}}
        self.app = Flask(__name__)
        self.api = Api(self.app,version='1.0.0',title=str('Space Fan Art (SFA)'),
                       description='This API, called SFA (Space Fan Art), is a fantastic API for any space fan.'
                                   'In essence, what this API does is to automatically put a fascinating '
                                   'image of planets and galaxy on your desktop background. The API is tailored'
                                   ' observing the best practices proven to secure a REST API. The SFA-API provides '
                                   'access via a web browser and has an interface, which allows authenticated users to '
                                   'not only download but also to upload images. ',
                       doc='/docs',authorizations=defining_authorizations)#docs é a rota q está direcionando para a API do swagger

    def run(self, ):
        self.app.run(debug=True,port=5003)


sfa_app = API()

#é preciso q os endpoints download e upload dependam da authentication key
# registro de usuário é o endpoint público (autentication)

#####################################################################################################################
#
#                                         MCV - Model-View-Controller
#
#   MVC is a software design pattern for user interfaces that divides the program into three elements:
#   MVC includes the model (data), the view (user interface), and the controller (processes that handle input)
#
#   ==> SFA - MVC:
#
#   M => The type of data we are using in the application: user's data and picture data (json)
#   V => Our interface (Html + Eel) and Swagger
#   C => It is in the file with 2 controllers (picture controller and user controller)
#
#####################################################################################################################


