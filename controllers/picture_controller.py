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

#########################################################################################
# Importing import sfa_app from minimal.py and storing in local variables
#########################################################################################

APP, SFA = sfa_app.app,sfa_app.api

# self.api =>> to configure all the API components - the routes, endpoints, methods, etc.
# self.app =>> deals with the application - checking in which door it is running, the rates, user login, etc.
# sfa_app ==> objet of the class API


#####################################################################################################################
#
#   VERSION 1 - contains one endpoint that allows users to download images (HTTP Request Type -> GET)
#
#####################################################################################################################

image_directory="images"

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
    @picture_namespace.doc(security='apikey') # telling swagger: "hey, this endpoint needs an api key"
    @api_or_demo_key_required # telling swagger: "hey, to the authentication created in this decorator" (from decorators.py)
    def get(self):
        """Downloads a picture"""
        cnxn = p.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
        cursor = cnxn.cursor()
        sql = 'SELECT top 1 Ima_Url from TB_SFA_Images order by NEWID()'
        cursor.execute(sql)
        result = cursor.fetchone()
        print(result[0])
        return send_from_directory(directory=os.path.dirname(result[0]),filename= os.path.basename(result[0]),as_attachment = True)
        #return send_from_directory(directory="\\".join(result[0].split("\\")[0:-1]),filename=result[0].split("\\")[-1],as_attachment=True)


#####################################################################################################################
#
#   VERSION 2 - contains one endpoint that allows authenticated users to upload an image (HTTP Request Type -> POST)
#
#####################################################################################################################

upload_parser = SFA.parser() # NOTE -> Parser will be defined for the API as a whole
upload_parser.add_argument('file', location='files', type=FileStorage, required=True)
upload_parser.add_argument('title', location='form', required=True)
upload_parser.add_argument('explanation', location='form', required=True)
upload_parser.add_argument('date',type = inputs.date_from_iso8601, location='form', required=True, help = "We expect data format of ISO 8601. Example: the date “September 7, 2019” is written as follows: “20190907”, or when expressed with delimiters: “2019-09-20”.")
upload_parser.add_argument('copyright', location='form', required=False)


###################################################################################################
# ===>>> Some clarifications:
#
# Parse() method parses arguments from an incoming request and uses as inputs to invoke the corresponding controller method
# The method .add_argument() is used to specify locations (as well as expected data type and whether or not the parameter is mandatory) to pull the values from the API
# In other words, it defines what information I'm going to get and where I'll get it from
# NOTE - > if parameter "required" is True, so if in the swagger I try to make the request without it I won't be able to
#####################################################################################################

#####################################################################################################
# ==>> The namespace decorator .route to define the endpoint upload in the API
# ==>> The namespace decorator .expect declares the parameters that the endpoint expects
#####################################################################################################
@picture_namespace.route('/api/v1/upload', doc={"description": 'user uploads an image'})
@picture_namespace.expect(upload_parser)
# Notice -> Decorator .expect  will show in swagger the file it is expecting to receive
# Notice -> Before running the class, it necessary to verify if the received request is as expected (this is what this decorator expect does!)
class Uploading(Resource): # The response method defines possible responses in the documentation
    @picture_namespace.response(200, 'Success')
    @picture_namespace.response(400, 'Request Error')
    @picture_namespace.response(500, 'Server Error')
    @picture_namespace.doc(security='apikey') # telling swagger: "hey, this endpoint needs an api key"
    @api_key_required # telling swagger: "hey, to the authentication created in this decorator" (from decorators.py

    def post(self):
        """Uploads a picture"""
        # The function parse_args() will execute parser inside the request. It extracts data from the file.
        args = upload_parser.parse_args()
        uploaded_file = args['file']  # This is FileStorage instance.
        # Now, saving in the directory images
        uploaded_file_title = args['title']
        uploaded_file_date = args['date']

        #####################################################################################################
        # ==>> OWASP C5: Validate All Inputs
        # ==>> OWASP C10: Handle All Errors and Exceptions
        #
        # NOTE: Here we use try-except statement for input validation.
        #####################################################################################################

        try:
            uploaded_file_date["date"] = validators.date(uploaded_file_date)
        except errors.EmptyValueError:
            print("Missing Input")
            return {"Error:": "Missing Input"}, 422
        except errors.CannotCoerceError:
            print("Invalid Input")
            return {"Error:": "Invalid Input"}, 422  # 422 - unprocessable entity"

        uploaded_file_explanation = args['explanation']
        uploaded_file_copyright = args['copyright']

        # Inserting the file in the API database
        PATH = os.path.abspath(os.path.dirname(__file__)) # This function receives a path and returns the absolute path on the pc

        # This function receives two parameters: the absolute and the relative path of the image
        uploaded_file_path = os.path.join(PATH, os.path.join('images', uploaded_file.filename))

        # Here the file is being saved inside the images folder
        uploaded_file.save("images/" + uploaded_file.filename)


        #########################################################################################################
        # ==> OWASP C3:Secure Database Access
        #
        # NOTE: Here we comply with OWASP by securing the access to the database considering:
        # a) Secure queries: To protect against SQL injection we use ‘Query Parameterization’
        # b) Secure configuration: we run the database in a docker container, which has connectivity restrictions
        # c) Secure communication: we use Pyodbc, an open source Python module to communicate with the database.
        #
        #########################################################################################################
        # Now we need to save the file path on the pc:
        cnxn = p.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
        cursor = cnxn.cursor()
        sql = f"""INSERT INTO TB_SFA_Images (Ima_Copyright, Ima_Date,Ima_Explanation,Ima_Title,Ima_Url) values (?,?,?,?,?)"""
        cursor.execute(sql, (uploaded_file_copyright, str(uploaded_file_date), uploaded_file_explanation, uploaded_file_title, uploaded_file_path))  # no ultimo argumento tem q ser o caminho absoluto
        cursor.commit()
        return {'Info': "Your file has been received!"}, 201

