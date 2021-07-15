from flask import request
from flask_restplus import fields, Resource
from minimal import sfa_app  # import the entire API
from validator_collection import validators, errors
import pyodbc as p
from senhas import *
from werkzeug.security import generate_password_hash, check_password_hash


#########################################################################################
# Importing import sfa_app from minimal.py and storing in local variables
#########################################################################################
APP, SFA = sfa_app.app, sfa_app.api
# self.api =>> to configure all the API components - the routes, endpoints, methods, etc.
# self.app =>> deals with the application - cheching in which door it is running, the rates, user loggin, etc.
# sfa_app ==> objet of the class API

#####################################################################################################################
#
#  v0.5.0 - Version 5 -Contains the first endpoint for GDPR: it allows users to see their personal data
#
#####################################################################################################################

#########################################################################################
# Creating a new namespace ==>> gdpr operations
# Namespaces are intended for organizing REST endpoints within the API.
#########################################################################################

gdpr_namespace = SFA.namespace('GDPR', description='GDPR operations')

#########################################################################################
# Creating a model for gdpr compliance
#########################################################################################

gdpr_model_request = SFA.model("gdpr model",{
    'email': fields.String,
    'password': fields.String})

#########################################################################################
# Here we place the namespace decorator .route to define the endpoint path within the API
#########################################################################################
@gdpr_namespace.route('/api/v1/gdpr1', doc={"description": 'user retrives personal data'})
class RetriveData(Resource):
# Resources are built on top of Flask pluggable views, giving access to HTTP methods (get, post, etc.)

    # Decorator @api.expect() allows you to specify the expected input fields.
    @gdpr_namespace.expect(gdpr_model_request)
    def post(self):
        # In this json file we will have email e password. EX.: {"email": "email@mail.com", "password": "125454678"}
        user_information = request.get_json()

        #####################################################################################################
        # ==>> OWASP C5: Validate All Inputs
        # ==>> OWASP C10: Handle All Errors and Exceptions
        #
        # NOTE: Here we use try-except statement for input validation.
        #####################################################################################################

        try:
            user_information["email"] = validators.email(user_information["email"])
            user_information["password"] = validators.not_empty(user_information["password"])
        except errors.EmptyValueError:
            print("Missing email")
            return {"Error:": "Missing email"}, 422 #unprocessable
        except errors.InvalidEmailError:
            print("Invalid email")
            return {"Error:": "Invalid email"}, 422 #unprocessable
        except:
            print("Payload error")
            return {"Error:": "Payload error"}, 422 #unprocessable


        #########################################################################################################
        # ==> OWASP C3:Secure Database Access
        #
        # Here we comply with OWASP by securing the access to the database considering:
        # a) Secure queries: To protect against SQL injection we use ‘Query Parameterization’
        # b) Secure configuration: we run the database in a docker container, which has connectivity restrictions
        # c) Secure communication: we use Pyodbc, an open source Python module to communicate with the database.
        #
        #  ===>>> Here we connect with the database to find the user_information: verify email and password
        #
        #########################################################################################################

        # ==>>> To find user_information email in the DB

        cnxn = p.connect(
            'DRIVER={ODBC Driver 17 for SQL Server};SERVER=' + server + ';DATABASE=' + database + ';UID=' + username + ';PWD=' + password)
        cursor = cnxn.cursor()
        sql = f""" SELECT * FROM [SFA_DB].[dbo].[TB_SFA_Registration] where [Reg_Email] = ?  COLLATE Latin1_General_CS_AS """
        cursor.execute(sql, (user_information["email"]))
        # NOTE: the second parameter is the value replacing the interrogation mark.

        ######################################################################################################
        # ==>> OWASP C5: Validate All Inputs
        # ==>> OWASP C10: Handle All Errors and Exceptions
        #
        # NOTE: Here we use try-except statement for input validation.
        ######################################################################################################

        try:
            results = []
            columns_names = [column[0] for column in cursor.description] # variable to store detailed values
            for row in cursor.fetchall():
                results.append(dict(zip(columns_names, row)))
            hashed_password = results[0]['Reg_Password']
        except:
            print("Invalid email")
            return {"Error:": "Invalid email"}, 401  # HTTP 401 - Unauthorized

        #########################################################################################################
        # ==> OWASP C6: Implement Digital Identity (Level 1 : Passwords)
        #
        # NOTE: Here we check if the password given by the user_information is correct.
        # The function used is werkzeug.check_password_hash(pwhash, password)
        # Parameters:
        # pwhash – a hashed string like returned by generate_password_hash().
        # password – the plaintext password to compare against the hash.
        #########################################################################################################

        # ==>>> to find out if user's password is in our DB

        if check_password_hash(hashed_password, user_information["password"]):
            results[0]['Reg_Expiration_Date'] = str(results[0]['Reg_Expiration_Date'])
            return results[0], 200 # HTTP 200 - Success
        print("Invalid password")
        return {"Error:": "Invalid password"}, 401  # HTTP 401 - Unauthorized

######################################################################################################################
#
#   v0.6.0 - Version 6 - Contains the second endpoint for GDPR: allows users to delete personal data stored in the DB
#
#######################################################################################################################

@gdpr_namespace.route('/api/v1/gdpr2', doc={"description": 'user deletes personal data'})
class DeleteData(Resource):
    # ex: email = request.form.get('email') #pega o email do formulario da request / verificar no banco
    @gdpr_namespace.expect(gdpr_model_request)
    def delete(self):
        user_information_to_delete = request.get_json()
        # user = request.get_json()  # nesse json terá email e password. # {"email": "email@mail.com", "password": "12345678"}
        try:
            user_information_to_delete["email"] = validators.email(user_information_to_delete["email"])
            user_information_to_delete["password"] = validators.not_empty(user_information_to_delete["password"])

        except errors.EmptyValueError:  # Handling logic goes here
            print("Missing email")
            return {"Error:": "Missing email"}, 422 #unprocessable
        except errors.InvalidEmailError:
            print("Invalid email")
            return {"Error:": "Invalid email"}, 422 #unprocessable
        except:
            print("Missing payload")
            return {"Error:": "Missing payload"}, 422


        #########################################################################################################
        # ==> OWASP C3:Secure Database Access
        #
        # Here we comply with OWASP by securing the access to the database considering:
        # a) secure queries: To protect against SQL injection we use ‘Query Parameterization’
        # b) we run the database in a docker container, which has connectivity restrictions
        # c) Secure communication: we use Pyodbc, an open source Python module to communicate with the database.
        #
        #  ===>>> Here we connect with the database to find the user_information: verify email and password
        #
        #########################################################################################################

        # ==>>> To find our if user's email in our DB

        cnxn = p.connect(
            'DRIVER={ODBC Driver 17 for SQL Server};SERVER=' + server + ';DATABASE=' + database + ';UID=' + username + ';PWD=' + password)
        cursor = cnxn.cursor()
        sql = f""" SELECT * FROM [SFA_DB].[dbo].[TB_SFA_Registration] where [Reg_Email] = ?  COLLATE Latin1_General_CS_AS """
        cursor.execute(sql, (user_information_to_delete["email"]))
        # NOTE: the second parameter is the value replacing the interrogation mark.

        ######################################################################################################
        # ==>> OWASP C5: Validate All Inputs
        # ==>> OWASP C10: Handle All Errors and Exceptions
        #
        # NOTE: Here we use try-except statement for input validation.
        ######################################################################################################

        try:
            results = []
            columns_names = [column[0] for column in cursor.description] # variable to store detailed values
            for row in cursor.fetchall():
                results.append(dict(zip(columns_names, row)))
            hashed_password = results[0]['Reg_Password']
        except:
            print("Invalid email")
            return {"Error:": "Invalid email"}, 401  # HTTP 401 - Unauthorized

        #########################################################################################################
        # ==> OWASP C6: Implement Digital Identity (Level 1 : Passwords)
        # Here we check if the password given by the user is correct.
        # The function used is werkzeug.check_password_hash(pwhash, password)
        #
        #########################################################################################################

        # CONNECTION WITH DB TO FIND THE USER: checking email and password to delete user

        if check_password_hash(hashed_password, user_information_to_delete["password"]):
            sql = f""" DELETE FROM [SFA_DB].[dbo].[TB_SFA_Registration] where [Reg_Email] = ?  COLLATE Latin1_General_CS_AS  """
            # The second parameter is the value that replaces the interrogation mark. This protects against injection
            deleted_row_count = cursor.execute(sql, (user_information_to_delete["email"])).rowcount
            cursor.commit() # this function is needed because we are making changes to the DB
            if deleted_row_count >0:
                return {"Info": "Your data was succcefully deleted from our database"}, 200  # HTTP 200 - Success
            else:
                return {"Error": "System could not delete the user"}, 422 #unprocessable
        return {"Error:": "Invalid password "}, 401 # HTTP 401 - Unauthorized
        # It will run the query and do the delete. It will get the numeber of columns affected.

        ########################################################################################################
        # ==> OWASP C3:Secure Database Access
        #
        # In the code above comply with OWASP by securing the access to the database considering:
        # a) secure queries: To protect against SQL injection we use ‘Query Parameterization’
        # b) we run the database in a docker container, which has connectivity restrictions
        # c) Secure communication: we use Pyodbc, an open source Python module to communicate with the database.
        #
        #########################################################################################################








