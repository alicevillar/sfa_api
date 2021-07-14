from datetime import date
from flask import request
from functools import wraps #os decoradores do python
import pyodbc as p
from senhas import *



#definindo um decorator q deve ficar antes de todos os ep q vao depender de chave de api
# o decorador sempre recebe como parametro a funçao q vem depois dele

# if de fora - qdo o usuario nao deu a chave
#if de dentro - qdo o usuario deu uma chave
def api_key_required(func):
    @wraps(func)
    def decorator(*args,**kwargs): #args - conjunto de parametros de posição / kwargs - parametros opcionais
        api_key = None
        if 'X-API-KEY' in request.headers: #se no header da request veio uma api key, salvo numa variável
            api_key = request.headers['X-API-KEY']
            # verificar se a chave que o usuário postou existe no banco de dados
            # select no bd para procurar a apikey
            cnxn = p.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=' + server + ';DATABASE=' + database + ';UID=' + username + ';PWD=' + password)
            cursor = cnxn.cursor()
            # Aqui nessa query será buscada a Reg_Authentication_Key, Reg_Id, Reg_Expiration_Date, Reg_Last_Access_Ip, Reg_Is_Blocked
            sql = f"""
                           SELECT Reg_Authentication_Key, Reg_Id, Reg_Expiration_Date, Reg_Last_Access_Ip, Reg_Is_Blocked FROM [SFA_DB].[dbo].[TB_SFA_Registration] where [Reg_Authentication_Key] = ? COLLATE Latin1_General_CS_AS 
                   """
            cursor.execute(sql,(api_key)) #o segundo parametro é o valor q substituirá a interrogaçao. Fica numa tupla
            result=cursor.fetchone()
            #print(result)
            if result == None: #assim comparo tipo com tipo
                return {'Info': 'Error: Invalid API KEY'}, 401  # dicionario e depois o status de resposta (note a aqui no restplus nao precisa do jsonify)
            else:
                is_blocked = result[4]
                expiration_date = result[2]
                last_access_ip = result[3]
                id_user = result[1]
                access_ip=request.remote_addr
                if is_blocked or date.today() > expiration_date or access_ip != last_access_ip:
                    sql = f""" DELETE from TB_SFA_Registration where Reg_Id = ?  """
                    cursor.execute(sql, (id_user))  # o segundo parametro é o valor q substituirá a interrogaçao. Fica numa tupla
                    cursor.commit()
                    # NOTE =>> a função api_key_required vai sempre rodar antes do endpoint
                    if access_ip != last_access_ip:
                        return {'Info': 'Error: You API Key is invalid because does not match your current IP. Please regiser again to create a new API Key.'}, 401
                    else:
                        return {'Info': 'Error: You API Key has expired or is blocked. Please regiser again to create a new API Key.'}, 401
                else:
                    return func(*args, **kwargs)  # aqui roda a funçao decorada - sucesso
        else:
            return {'Info':'Error: missing API KEY'},401 #dicionario e depois o status de resposta (note a aqui no restplus nao precisa do jsonify)
    return decorator

# O usuário q estiver com chave expirada, está bloqueado ou ip diferente vai tentar entrar e será deletado no banco. Ele vai receber uma mensagem de q nao pode.

#####################################
#
# Creating a decorator for the demo key and api
#
######################################

def api_or_demo_key_required(func): # This decorator has both the DEMO KEY and the API KEY
    @wraps(func)
    def decorator(*args,**kwargs): #args - conjunto de parametros de posição / kwargs - parametros opcionais
        api_key = None
        if 'X-API-KEY' in request.headers: #se no header da request veio uma api key, salvo numa variável

            api_key = request.headers['X-API-KEY']
            #print(api_key)
            if api_key == demo_key: # Checking if the key received is the demokey
                return func(*args, **kwargs)  # aqui roda a funçao decorada - sucesso
            else: # BLOCO DO DECORADOR ANTERIOR:
                # verificar se a chave que o usuário postou existe no banco de dados
                # select no bd para procurar a apikey
                cnxn = p.connect(
                    'DRIVER={ODBC Driver 17 for SQL Server};SERVER=' + server + ';DATABASE=' + database + ';UID=' + username + ';PWD=' + password)
                cursor = cnxn.cursor()
                # Aqui nessa query será buscada a Reg_Authentication_Key, Reg_Id, Reg_Expiration_Date, Reg_Last_Access_Ip, Reg_Is_Blocked
                sql = f"""
               SELECT Reg_Authentication_Key, Reg_Id, Reg_Expiration_Date, Reg_Last_Access_Ip, Reg_Is_Blocked FROM [SFA_DB].[dbo].[TB_SFA_Registration] where [Reg_Authentication_Key] = ? COLLATE Latin1_General_CS_AS 
                                   """
                cursor.execute(sql,
                               (api_key))  # o segundo parametro é o valor q substituirá a interrogaçao. Fica numa tupla
                result = cursor.fetchone()
                #print("imprimindo resultado api key")
                #print(result)
                if result == None:  # assim comparo tipo com tipo
                    return {
                               'Info': 'Error: Invalid API KEY'}, 401  # dicionario e depois o status de resposta (note a aqui no restplus nao precisa do jsonify)
                else:
                    is_blocked = result[4]
                    expiration_date = result[2]
                    last_access_ip = result[3]
                    id_user = result[1]
                    access_ip = request.remote_addr
                    if is_blocked or date.today() > expiration_date or access_ip != last_access_ip:
                        sql = f""" DELETE from TB_SFA_Registration where Reg_Id = ?  """
                        cursor.execute(sql, (
                            id_user))  # o segundo parametro é o valor q substituirá a interrogaçao. Fica numa tupla
                        cursor.commit()
                        # NOTE =>> a função api_key_required vai sempre rodar antes do endpoint
                        if access_ip != last_access_ip:
                            return {
                                       'Info': 'Error: You API Key is invalid because does not match your current IP. Please regiser again to create a new API Key.'}, 401
                        else:
                            return {
                                       'Info': 'Error: You API Key has expired or is blocked. Please regiser again to create a new API Key.'}, 401
                    else:
                        return func(*args, **kwargs)  # aqui roda a funçao decorada - sucesso
        # FECHANDO BLOCO DO DECORADOR
        else:
            return {'Info':'Error: missing API KEY'},401 #dicionario e depois o status de resposta (note a aqui no restplus nao precisa do jsonify)

    return decorator

