from flask import send_from_directory, request
from flask_restplus import Api, Resource, fields, inputs
from validator_collection import validators, errors
from minimal import sfa_app
import pyodbc as p
import os
from werkzeug.datastructures import FileStorage
from senhas import *
from decorators import *
from controllers.limiters_controller import *
import requests

#########################################################################################
# Importing import sfa_app from minimal.py and storing in local variables
#########################################################################################

APP, SFA = sfa_app.app,sfa_app.api
# self.api =>> to configure all the API components - the routes, endpoints, methods, etc.
# self.app =>> deals with the application - checking in which door it is running, the rates, user login, etc.
# sfa_app ==> objet of the class API

#####################################################################################################################
#
#   VERSION 7 - contains one endpoint that allows users to get images from NASA API APOD (HTTP Request Type -> GET)
#
#####################################################################################################################

#########################################################################################
# First step => Creating a new namespace: pictures. It is used for download and upload.
#########################################################################################

picture_namespace = SFA.namespace('Pictures', description='Picture operations')
# Namespaces are intended for organizing REST endpoints within the API.
# The main idea is to split the app into reusable namespaces.

#############################################################################################
# Here we place the namespace decorator .route to define the endpoint download in the API
#############################################################################################

@picture_namespace.route('/api/v1/download', doc={"description": 'user downloads an image'})
class Downloading(Resource):
    # The response method defines possible responses in the documentation:
    @picture_namespace.response(200, 'Success')
    @picture_namespace.response(400, 'Request Error')
    @picture_namespace.response(500, 'Server Error')
    @picture_namespace.doc(security='apikey') # telling swagger: "this endpoint needs an api key"
    @api_or_demo_key_required # telling swagger: "hey, to the authentication created in this decorator" (from decorators.py)
    def get(self):
        """Downloads a picture"""
        response = requests.get(url_apod)  # another way to do it: return requests.get(url_apod).json()
        response = response.json()
        return response




