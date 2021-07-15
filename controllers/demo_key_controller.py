from flask import Flask, jsonify, request, send_from_directory
from flask_restplus import Api, Resource, fields, inputs
from minimal import sfa_app
from senhas import *

########################################################################################
# Importing import sfa_app from minimal.py and storing in local variables
########################################################################################

APP, SFA = sfa_app.app,sfa_app.api
# self.api =>> to configure all the API components - the routes, endpoints, methods, etc.
# self.app =>> deals with the application - checking in which door it is running, the rates, user login, etc.
# sfa_app ==> objet of the class API

#################################################################################################################
#
#   v0.4.0 - Version 4 - Contains one endpoint to create the demo key (HTTP Request Type -> GET)
#
##################################################################################################################

#########################################################################################
# First step => Creating a new namespace: demo
#########################################################################################
demo_key_namespace = SFA.namespace('Demo Key', description='Demo Key operations')

# Here we create a namespace for demo key operations.
# Namespaces are intended for organizing REST endpoints within the API.

#############################################################################################
# Here we place the namespace decorator .route to define the endpoint path within the API
#############################################################################################
@demo_key_namespace.route('/api/v1/demo_key', doc={"description": 'Retriving Demo Key'})
class Demo_Key_Registration(Resource):
    # The response method defines possible responses in the documentation
    @demo_key_namespace.response(200, 'Success')
    @demo_key_namespace.response(400, 'Request Error')
    @demo_key_namespace.response(500, 'Server Error')
    # o metodo posto tem q garantir q aquilo q ele recebe como parametro é o modelo de usuário

    def get(self): # Generating demo key
        return {"API Key": demo_key}, 200






