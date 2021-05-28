from flask import Flask, jsonify, request, send_from_directory
from flask_restplus import Api, Resource, fields, inputs
from minimal import sfa_app
import pyodbc as p
import json as js
import os
from werkzeug.datastructures import FileStorage #importando uma abstração de arquivo
from senhas import *

#####################################################################################################################
#
#   VERSION 1 - contains one endpoint that allows you to download an image (HTTP Request Type -> GET)
#
#####################################################################################################################


image_directory="images"
# Importing and storing in local variables
APP, SFA = sfa_app.app,sfa_app.api

# Namespaces are intended for organizing REST endpoints within the API.
# The main idea is to split the app into reusable namespaces.

picture_namespace = SFA.namespace('pictures', description='picture operations')

# The decorator .route defines the endpoint path within the API
@picture_namespace.route('/api/v1/download', doc={"description": 'user downloads an image'})

class Downloading(Resource):
    # The response method defined possible responses in the documentation
    @picture_namespace.response(200, 'Success')
    @picture_namespace.response(400, 'Request Error')
    @picture_namespace.response(500, 'Server Error')
    #The .expect declares the parameters (mandatory or not) that the endpoint expects
    # @namespace.expect(create_producer_request, validate=True)
    # o .marshal_with declara a estrutura da resposta com base no model recebido como parâmetro
    # @namespace.marshal_with(create_producer_response)

    def get(self):
        """Downloads a picture"""
        cnxn = p.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
        cursor = cnxn.cursor()
        sql = 'SELECT top 1 Ima_Url from TB_SFA_Images order by NEWID()'
        cursor.execute(sql)
        result=cursor.fetchone()
        print(result[0])
        return send_from_directory(directory="\\".join(result[0].split("\\")[0:-1]),filename=result[0].split("\\")[-1],as_attachment=True)


#####################################################################################################################
#
#   VERSION 2 - contains one endpoint that allows authenticated users to upload an image (HTTP Request Type -> POST)
#
#####################################################################################################################

# Parse() method parses arguments from an incoming request and uses them as inputs to invoke the corresponding controller method
# The method .add_argument() is used to specify locations to pull the values from the API
# In other words, it defines what information I'm going to get and where I'll get it from

upload_parser = SFA.parser() # NOTE -> Parser will be defined for the API as a whole
upload_parser.add_argument('file', location='files', type=FileStorage, required=True)
upload_parser.add_argument('title', location='form', required=True)
upload_parser.add_argument('explanation', location='form', required=True)
upload_parser.add_argument('date',type = inputs.date_from_iso8601, location='form', required=True)
upload_parser.add_argument('copyright', location='form', required=False)

# NOTE - > if parameter "required" is True, so if in the swagger I try to make the request without it I won't be able to

# Namespaces are intended for organizing REST endpoints within the API.
# The main idea is to split the app into reusable namespaces.
@picture_namespace.route('/api/v1/upload', doc={"description": 'user uploads an image'})

# The .expect method declares the parameters (mandatory or not) that the endpoint expects
@picture_namespace.expect(upload_parser) # Note -> It will show in swagger the file it is expecting to receive


class Uploading(Resource):
    # The response method defined possible responses in the documentation
    @picture_namespace.response(200, 'Success')
    @picture_namespace.response(400, 'Request Error')
    @picture_namespace.response(500, 'Server Error')
     # @picture_namespace.expect(create_producer_request, validate=True)
    # o .marshal_with declara a estrutura da resposta com base no model recebido como parâmetro
    # @namespace.marshal_with(create_producer_response)

    def post(self):
        """Uploads a picture"""
        # The function parse_args() will execute parser inside the request. It extracts data from the file.
        args = upload_parser.parse_args()
        uploaded_file = args['file']  # This is FileStorage instance.
        # Agora, saving in the directory images
        uploaded_file_title = args['title']
        uploaded_file_date = args['date']
        uploaded_file_explanation = args['explanation']
        uploaded_file_copyright = args['copyright']

        # NOTE -> in any of these fields, if a user tries to insert a malicious code, he will not succseed.
        # The library already has a syntax that does the protection.

        # Inserting the file in the API database

        PATH = os.path.abspath(os.path.dirname(__file__)) # This function receives a path and returns the absolute path on the pc

        # This function receives two parameters: the absolute and the relative path of the image
        uploaded_file_path = os.path.join(PATH, os.path.join('images', uploaded_file.filename))

        # Here the file is being saved inside the images folder
        uploaded_file.save("images/" + uploaded_file.filename)

        # Now you need to save the file path on the pc
        cnxn = p.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
        cursor = cnxn.cursor()
        sql = f"""
            INSERT INTO TB_SFA_Images (Ima_Copyright, Ima_Date,Ima_Explanation,Ima_Title,Ima_Url) 
            values (?,?,?,?)"""
        cursor.execute(sql, (uploaded_file_copyright, uploaded_file_date, uploaded_file_explanation, uploaded_file_title, uploaded_file_path))  # no ultimo argumento tem q ser o caminho absoluto
        cursor.commit()
        # url = do_something_with_file(uploaded_file)
        return {'Info': "Your file has been received!"}, 201

        # NOTE -> The library already has a syntax that protects against SQL injection.
