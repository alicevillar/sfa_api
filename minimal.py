from flask import Flask
from flask_restplus import Resource, Api
from controllers.picture_controller import *
from flask import Flask, request
from flask_restplus import Api


class API():
    def __init__(self, ):
        self.app = Flask(__name__)
        self.api = Api(self.app,version='1.0.0',title=str('Space Fan Art (SFA)'),description='This API, called SFA (Space Fan Art), is a fantastic API for any space fan. In essence, what this API does is to automatically put a fascinating image of planets and galaxy on your desktop background. The API is tailored observing the best practices proven to secure a REST API. The SFA-API provides access via a web browser and has an interface, which allows authenticated users to not only download but also to upload images. ',doc='/docs')#docs é a rota q está direcionando para a API do swagger

    def run(self, ):
        self.app.run(debug=True)

sfa_app = API()

#na pasta controllers terao dois grupos: o grupo de apis relacionadas a imagem e o grupo relacionado a usuário mvc
# (M = o tipo de dado q estamos usando na aplicaçao / ex.: dado usuário e dado picture - json
# ( V (tkinter/swagger) C(está na parts com 2 controladores, q vao fazer as operacoes do BD -> upload-insert/ download-select )