from flask import Flask
from flask_restplus import Resource, Api
from flask import Flask, request
from flask_restplus import Api
from flask_cors import CORS


class API():
    def __init__(self):
        defining_authorizations = {'apikey':  {'type': 'apiKey','in': 'header', 'name': 'X-API-KEY'}}
        self.app = Flask(__name__)
        CORS(self.app, resources={r"/*": {"origins": "*"}}) # this function has one parameter app (the instance) and resources, which defines how the api will respond to other origins.
        self.app.secret_key = 'super secret string'
        self.api = Api(self.app,version='1.0.0',title=str('Space Fan Art (SFA)'),
                       description='This API, called SFA (Space Fan Art), is an API created with Flask REST-Plus following the best practices proven to secure a REST-API and showcasing the OWASP Top Ten Proactive Controls. Users have to register to get an authentication key, which allows them to download and upload images from NASA',
                       doc='/docs',authorizations=defining_authorizations) # docs is the route that is going to the swagger API

    def run(self, ):
        self.app.run(debug=True,port=5000) # linking the container with mine (127.001)
#==>> to run the api with docker use port=5000,host="0.0.0.0"
#==>> to run the api in my pc use port=5001, no need to include host because it will be the default (my ip)

# variable sfa_app ==> objet of the class API
sfa_app = API()

#####################################################################################################################
#
#                                         MCV - Model-View-Controller
#
#   The Model-View-Controller (MVC) framework is an architectural pattern that separates an application
#   into 3 main logical components: model (data), view (user interface), and controller (processes that handle input)
#
#   ==> SFA - MVC:
#
#   Model => The type of data we are using in the application: user's data and picture data (json)
#   View => Our interfaces (Html/CSS/Javascript) and Swagger
#   Controller => In the file with 6 controllers
#
#####################################################################################################################

