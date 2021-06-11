
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


#date dá a data de hj e o delta p/ add dias

# um endpoint para receber os dados do usuário
# um end point para o usuário - GDPR - deletar, zerar, revogar autorizacao de uso dos dados, consultar(Get-selct)


#####################################################################################################################
#
#   VERSION 1 - contains one endpoint  para receber os dados do usuário
#
#####################################################################################################################


# Importing and storing in local variables
APP, SFA = sfa_app.app,sfa_app.api

# Namespaces are intended for organizing REST endpoints within the API.
# The main idea is to split the app into reusable namespaces.

users_namespace = SFA.namespace('users', description='user operations')


# criando um modelo de usuario
user_model_request = SFA.model("user model",{
    'First Name': fields.String,
    'Last Name': fields.String,
    'Email': fields.String,
    'Password': fields.String})

user_model_response = SFA.model("response",{'API Key': fields.String,'Expiration Date':fields.String} )


#####################################################################################################################
#
#   VERSION 3 - contains one endpoint that creates authentication key (HTTP Request Type -> POST)
#
#####################################################################################################################

# The decorator .route defines the endpoint path within the API
@users_namespace.route('/api/v1/register', doc={"description": 'user authentication'})

class Registration(Resource):
    # The response method defined possible responses in the documentation
    @users_namespace.response(200, 'Success')
    @users_namespace.response(400, 'Request Error')
    @users_namespace.response(500, 'Server Error')
    # o metodo posto tem q garantir q aquilo q ele recebe como parametro é o modelo de usuário
    @users_namespace.marshal_with(user_model_response) #marshal with: a) mostra no swager o modelo de resposta
    #b) checa se a funcao q estou implementando no endpoint está de acordo com o modelo

    # The .expect method declares the parameters (mandatory or not) that the endpoint expects
    @users_namespace.expect(user_model_request)  # Note -> It will show in swagger the file it is expecting to receive

    def post(self): # Generate api key
        # extrair essas infomacoes da request, então ler os 3 parametros da request e inserir no bd
        #new user recebe um dicionário, entao vou usar isso para inserir no bc esses valores
        new_user=request.get_json()

        #usando a bibl secrets para gerar chave de api
        apikey=secrets.token_urlsafe(30)

        expiration_date=date.today()+ timedelta(days=30)
        is_blocked=False
        access_ip=request.remote_addr #CAPTURANDO o IP de onde vem o request
        password_hash= generate_password_hash(new_user['Password'])
        #para verificar se está correta a senha será: check_password_hash(hash," - senha recebida p/ verificação - ")


        """User Registration"""
        cnxn = p.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
        cursor = cnxn.cursor()
        sql = f""" INSERT INTO TB_SFA_Registration (Reg_Name,Reg_LastName,Reg_Email,Reg_Authentication_Key,Reg_Password,Reg_Expiration_Date,Reg_Last_Access_Ip,Reg_Is_Blocked) 
        values (?,?,?,?,?,?,?,?)"""
        cursor.execute(sql, (new_user['First Name'],new_user['Last Name'],new_user['Email'],apikey, password_hash,expiration_date,access_ip,is_blocked))
        cursor.commit() # para de fato executar o comando
        #result=cursor.fetchone()
        #print(result[0])
        return {"API Key": apikey,"Expiration Date":expiration_date}, 200




