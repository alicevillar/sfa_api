from flask import Flask, jsonify, request, send_from_directory
from flask_restplus import Api, Resource, fields
from minimal import sfa_app
import pyodbc as p
import json as js
import os

image_directory="images"

'''
    Modelo geral de operacao em recurso de uma API REST
'''
#importando e guardando em varia'veis locais
APP, SFA = sfa_app.app,sfa_app.api

picture_namespace = SFA.namespace('pictures', description='picture operations')

# O decorador .route define o caminho do endpoint dentro da API
@picture_namespace.route('/download', doc={"description": 'user downloads an image'})
#@picture_namespace.param('id', 'Identificador único do produtor')
# o decorador .expect declara as configurações, obrigatórias ou não, que devem ser enviadas
# @namespace.expect(headers)

class Downloading(Resource):
    # O response deixa explícito na documentação as possíveis respostas
    @picture_namespace.response(200, 'Success')
    @picture_namespace.response(400, 'Request Error')
    @picture_namespace.response(500, 'Server Error')
    # O .expect declara os parâmetros, obrigatórios ou não, que o endpoit espera
    # @namespace.expect(create_producer_request, validate=True)
    # o .marshal_with declara a estrutura da resposta com base no model recebido como parâmetro
    # @namespace.marshal_with(create_producer_response)

    def get(self):
        """Downloads a picture"""
        server = 'ALICE-PC'
        database = 'SFA_DB'
        username = 'sa'
        password = 'Anandamayi2018'
        cnxn = p.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
        cursor = cnxn.cursor()

        sql='SELECT top 1 Ima_Url from TB_SFA_Images order by NEWID()'
        cursor.execute(sql)
        result=cursor.fetchone()
        print(result[5])
        #return send_from_directory(image_directory,result[5].split('/')[-1],as_attachment=True) #recebe o caminho e retorna na requisição
        return send_from_directory(directory="\\".join(result[5].split("\\")[0:-1]),filename=result[5].split("\\")[-1],as_attachment=True)


