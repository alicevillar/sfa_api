from datetime import date
from flask import request
from functools import wraps #os decoradores do python
import pyodbc as p
from senhas import *

################################################################################################################
#                               OWASP C6: Implementing Digital Identity
# Level 1 : Passwords
# Level 2 = Multi-Factor Authentication (MFA) = applies 2 layers of protection: passwords and authentication key.
# Level 3 = Cryptographic Based Authentication
#
#                                    OWASP C7: Enforce Access Controls

# The multi-factor authentication in 2 layers of protection: hashing passwords and authentication key.
# Here the authentication key is following these rules:
# a) expiration date – SFA-API has an expiration date, which is done using pyodbc;
# b) rate limits - The requests per IP address have the following limits: 80 per day/80 per hour.
# c) user IP – The system creates a key that corresponds the client’s IP.
# If the same client changes IP and tries to authenticate, the system doesn't allow and will asks to authenticate again.
#
#                               OWASP C9: Implement Security Logging and Monitoring
#
# In SFA-API, we use the logging framework, a utility to standardise the process of logging in your application.
# It provides a coherent collection of decorators and tools to describe your API and expose its documentation properly (using Swagger).
#
#                                           OWASP C3:Secure Database Access
#
# NOTE: Here we comply with OWASP by securing the access to the database considering:
# a) Secure queries: To protect against SQL injection we use ‘Query Parameterization’
# b) Secure configuration: we run the database in a docker container, which has connectivity restrictions
# c) Secure communication: we use Pyodbc, an open source Python module to communicate with the database.
#
#########################################################################################################


##############################################################################################################
#
#                                   DECORATOR: api_key_required
#
# Here we define a decorator that must be before all endpoints will depend on api key
# NOTE =>> the api_key_required function will always run before the endpoint
#
################################################################################################################

def api_key_required(func):
    @wraps(func)
    def decorator(*args,**kwargs):
        #*args and **kwargs are special keyword which allows function to take variable length argument.
        # **kwargs - optional parameters. *args and **kwargs make the function flexible.
        api_key = None

        ###############################################################################################################
        #
        #         THE FOLLOWING BLOCKS OF CODE ARE ORGANIZED LIKE THIS:
        #
        #         # OUTSIDE "IF" ==>> when user did not provide a key
        #         # INSIDE "IF" ==>> when user provided a key
        ###################################################################################################

        if 'X-API-KEY' in request.headers: # If in the request header came an api key, I save it in a variable
            api_key = request.headers['X-API-KEY']
            # verify if the key the user posted exists in the database
            # select in database to search for apikey
            cnxn = p.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=' + server + ';DATABASE=' + database + ';UID=' + username + ';PWD=' + password)
            cursor = cnxn.cursor()
            # this query is protected against sql injection:
            sql = f"""
                           SELECT Reg_Authentication_Key, Reg_Id, Reg_Expiration_Date, Reg_Last_Access_Ip, Reg_Is_Blocked FROM [SFA_DB].[dbo].[TB_SFA_Registration] where [Reg_Authentication_Key] = ? COLLATE Latin1_General_CS_AS 
                   """
            cursor.execute(sql,(api_key)) # the second parameter is the value that replaces the interrogation mark
            result=cursor.fetchone()
            #print(result)
            if result == None: # if there is no apy key:
                return {'Info': 'Error: Invalid API KEY'}, 401  # (note that with flask rest plus we don't need jsonify)

            ###############################################################################################################
            #
            #     THE FOLLOWING BLOCKS OF CODE:
            #     # The user who has an expired key, is blocked or is trying to authenticate with a different IP:
            #     ===>>will be deleted from the DB. If he tried do enter, he will receive a message saying that it not allowed.
            #
            ###################################################################################################

            else:
                is_blocked = result[4]
                expiration_date = result[2]
                last_access_ip = result[3]
                id_user = result[1]
                access_ip=request.remote_addr
                if is_blocked or date.today() > expiration_date or access_ip != last_access_ip:
                    sql = f""" DELETE from TB_SFA_Registration where Reg_Id = ?  """
                    cursor.execute(sql, (id_user)) # the second parameter is the value that replaces the interrogation mark
                    cursor.commit()

                    if access_ip != last_access_ip:
                        return {'Info': 'Error: You API Key is invalid because does not match your current IP. Please regiser again to create a new API Key.'}, 401
                    else:
                        return {'Info': 'Error: You API Key has expired or is blocked. Please regiser again to create a new API Key.'}, 401
                else:
                    return func(*args, **kwargs)  # running the decorated function
        else:
            return {'Info':'Error: missing API KEY'},401 # here goes a dictionary and then the http response (here in restplus we do not need jsonify :) )
    return decorator


##############################################################################################################
#
#                                   DECORATOR: api_or_demo_key_required
#
# Here we are creating a decorator for both the DEMO KEY and the API KEY
#
################################################################################################################


def api_or_demo_key_required(func):
    @wraps(func)
    def decorator(*args,**kwargs): # args - set of position parameters / kwargs - optional parameters
        api_key = None
        if 'X-API-KEY' in request.headers: # if the request header comes with an api key, save it in a variable
            api_key = request.headers['X-API-KEY']
            #print(api_key)
            if api_key == demo_key: # Checking if the key received is the demo key
                return func(*args, **kwargs)

            # NOW THE FOLLOWING BLOCK OF CODE COMES FROM THE PREVIOUS DECORATOR:
            else:
                # verify that the key the user posted exists in the database
                # select db to search for apikey
                cnxn = p.connect(
                    'DRIVER={ODBC Driver 17 for SQL Server};SERVER=' + server + ';DATABASE=' + database + ';UID=' + username + ';PWD=' + password)
                cursor = cnxn.cursor()
                sql = f"""
               SELECT Reg_Authentication_Key, Reg_Id, Reg_Expiration_Date, Reg_Last_Access_Ip, Reg_Is_Blocked FROM [SFA_DB].[dbo].[TB_SFA_Registration] where [Reg_Authentication_Key] = ? COLLATE Latin1_General_CS_AS 
                                   """
                cursor.execute(sql,
                               (api_key))
                result = cursor.fetchone()
                #print("imprimindo resultado api key")
                #print(result)
                if result == None:
                    return {
                               'Info': 'Error: Invalid API KEY'}, 401
                else:
                    is_blocked = result[4]
                    expiration_date = result[2]
                    last_access_ip = result[3]
                    id_user = result[1]
                    access_ip = request.remote_addr
                    if is_blocked or date.today() > expiration_date or access_ip != last_access_ip:
                        sql = f""" DELETE from TB_SFA_Registration where Reg_Id = ?  """
                        cursor.execute(sql, (
                            id_user))
                        cursor.commit()

                        if access_ip != last_access_ip:
                            return {
                                       'Info': 'Error: You API Key is invalid because does not match your current IP. Please regiser again to create a new API Key.'}, 401
                        else:
                            return {
                                       'Info': 'Error: You API Key has expired or is blocked. Please regiser again to create a new API Key.'}, 401
                    else:
                        return func(*args, **kwargs)  # Running the decorated function - success
        # CLOSING THE BLOCK
        else:
            return {'Info':'Error: missing API KEY'},401 # notice this syntax: dictionary and then the response (Here in Restplus we don't need jsonify :) )

    return decorator

