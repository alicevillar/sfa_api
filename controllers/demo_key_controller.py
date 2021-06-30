
from flask import Flask, jsonify, request, send_from_directory
from flask_restplus import Api, Resource, fields, inputs
from minimal import sfa_app
import pyodbc as p
import json as js
import os
from werkzeug.datastructures import FileStorage #importando uma abstração de arquivo
from senhas import *
import secrets
from datetime import date,timedelta
from werkzeug.security import generate_password_hash,check_password_hash


#####################################################################################################################
#
#   VERSION 3 - contains one endpoint that creates a demo key
#
#####################################################################################################################


# Importing and storing in local variables
APP, SFA = sfa_app.app,sfa_app.api

demo_key_namespace = SFA.namespace('demo', description='demo operations')

# The decorator .route defines the endpoint path within the API
@demo_key_namespace.route('/api/v1/demo_key', doc={"description": 'Retriving Demo Key'})



class Demo_Key_Registration(Resource):
    # The response method defined possible responses in the documentation
    @demo_key_namespace.response(200, 'Success')
    @demo_key_namespace.response(400, 'Request Error')
    @demo_key_namespace.response(500, 'Server Error')
    # o metodo posto tem q garantir q aquilo q ele recebe como parametro é o modelo de usuário

    def get(self): # Generate demo key
        return {"API Key": demo_key}, 200






