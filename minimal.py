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
        self.app.secret_key = 'super secret string' # gerenciamento de sessão para guardar info e poder usar p/ o login
        self.api = Api(self.app,version='1.0.0',title=str('Space Fan Art (SFA)'),
                       description='This API, called SFA (Space Fan Art), is an API created with Flask REST-Plus following the best practices proven to secure a REST-API and showcasing the OWASP Top Ten Proactive Controls. Users have to register to get an authentication key, which allows them to download and upload images from NASA',
                       doc='/docs',authorizations=defining_authorizations)#docs é a rota q está direcionando para a API do swagger

    def run(self, ):
        self.app.run(debug=True,port=5000)

# a variável self.api =>> aonde configura rotas, endpoints, métodos, etc. Todos os componentes da api
# a variável self.app =>> lida com a aplicação: em que porta está rodando, verificar o rates todos, loggin dos usuários
# a variável sfa_app ==> objeto da classe

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


