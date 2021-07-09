from flask import request
import flask_login
from flask_restplus import fields, Resource
from minimal import sfa_app  # importanto a API inteira
from validator_collection import validators, errors
import pyodbc as p
from senhas import *
from werkzeug.security import generate_password_hash, check_password_hash

#####################################################################################################################
#
#   VERSION 5 - contains one endpoint that creates the sign in
#
#####################################################################################################################



# a variável self.api =>> aonde configura rotas, endpoints, métodos, etc. Todos os componentes da api
# a variável self.app =>> lida com a aplicação: em que porta está rodando, verificar o rates todos, loggin dos usuários
# a variável sfa_app ==> objeto da classe


# login_manager é agora pode funcionar como um decorador para decorar endpoints que precisa de login qto para logar usuário e deslogar
login_manager = flask_login.LoginManager()  # será usado como decorador para controlar o login
APP, SFA = sfa_app.app, sfa_app.api
login_manager.init_app(APP)  # sintaxe de configuração

login_logout_users_namespace = SFA.namespace('login/logout', description='login/logout operations')

# criando um modelo de usuario
login_logout_model_request = SFA.model("login/logout model", {
    'email': fields.String,
    'password': fields.String})


@login_logout_users_namespace.route('/api/v1/login_logout', doc={"description": 'user login/logout'})

class User(
    flask_login.UserMixin):  # This provides default implementations for the methods that Flask-Login expects user objects to have.
    pass


# UserMixin tem muitos métodos uteis para retornar se o usuário está logado e se está autenticado. É recomendação da biblioteca usar
# Esse método vai ser executado qdo o endpoint precisar identificar quem é o usuário
# Objetivo dessa função é saber que usuário está fazendo a request. Essa função nao vem pronta, tem q implementar
@login_manager.request_loader  # está avisando q a função abaixo tem q retornar um objeto usuário
def request_loader(request):
    # ex: email = request.form.get('email') #pega o email do formulario da request / verificar no banco
    user = request.get_json()  # nesse json terá email e password. # {"email": "email@mail.com", "password": "12345678"}
    try:
        user["email"] = validators.email(user["email"])
        user["password"] = validators.not_empty(user["password"])

    except errors.EmptyValueError:  # Handling logic goes here
        print("Missing email")
        return
    except errors.InvalidEmailError:
        print("Invalid email")
        return

    # CONNECTION WITH DB TO FIND THE USER: VERIFICAR EMAIL E SENHA
    cnxn = p.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};SERVER=' + server + ';DATABASE=' + database + ';UID=' + username + ';PWD=' + password)
    cursor = cnxn.cursor()

    # Aqui nessa query será buscada a Reg_Authentication_Key, Reg_Id, Reg_Expiration_Date, Reg_Last_Access_Ip, Reg_Is_Blocked
    sql = f"""SELECT Reg_Id FROM [SFA_DB].[dbo].[TB_SFA_Registration] where [Reg_Email] = ? COLLATE Latin1_General_CS_AS """

    cursor.execute(sql, (user["email"]))  # o segundo parametro é o valor q substituirá a interrogaçao. Fica numa tupla
    result = cursor.fetchone()  # essa variável vai retornar o ID do usuário e o hash da senha do usuário (tupla)
    reg_id = result[0]
    hashed_password = result[1]

    # VERIFICAR SE O PASSWORD DO USUÁRIO ESTÁ CORRETO

    # FUNção usada: werkzeug.check_password_hash(pwhash, password)
    # Parameters:
    # pwhash – a hashed string like returned by generate_password_hash().
    # password – the plaintext password to compare against the hash.

    user_loggin = User()
    user_loggin.id = reg_id  # o primeiro campo retornado é o ID do usuário, e o segundo será o hashed password

    if check_password_hash(hashed_password, user["password"]):
        user_loggin.is_authenticated = True  # is_authenticated is an atribute of UserMixin
        return user_loggin
    print("Invalid password")
    return


class login(Resource):  # esse Resource é a rota
    # The response method defined possible responses in the documentation
    @login_logout_users_namespace.response(200, 'Success')
    @login_logout_users_namespace.response(400, 'Request Error')
    @login_logout_users_namespace.response(500, 'Server Error')
    # o metodo post tem q garantir q aquilo q ele recebe como parametro é o modelo de usuário

    # The .expect method declares the parameters (mandatory or not) that the endpoint expects
    @login_logout_users_namespace.expect(
        login_logout_model_request)  # Note -> It will show in swagger the file it is expecting to receive
    def post(self):  # Generate api key
        # extrair essas infomacoes da request, então ler os 3 parametros da request e inserir no bd
        # new user recebe um dicionário, entao vou usar isso para inserir no bc esses valores
        user_credentials = request_loader(request)
        if user_credentials != None:
            flask_login.login_user(user_credentials)
            return {"Success:": "Valid Credentials"}, 200
        return {"Error:": "Invalid Credentials"}, 422
