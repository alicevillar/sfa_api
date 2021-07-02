from flask import request


# Protecting against DDOs attacks

from flask import Flask
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from minimal import sfa_app

# Limiter - IP

APP, SFA = sfa_app.app,sfa_app.api

ip_limiter = Limiter(
    APP,
    key_func=get_remote_address, # counting the use. This functions returns the IP, so it can recognize when the same IP uses the API more than x times
    default_limits=["50 per day", "50 per hour"]
)

# função para auxiliar a biblioteca de limitação. Essa função vai fazer uma contagem do numero de requests por chave
def get_key():
    try:
        api_key = request.headers['X-API-KEY']
        return api_key

    except: # se não foi forcencida uma api key: #avisar no terminal um det erro.
        raise Exception('Request done with no API Key. Limiting could no be done')

key_usage_limiter = Limiter(
    APP,
    key_func=get_key, # counting the use. This functions returns the IP, so it can recognize when the same IP uses the API more than x times
    default_limits=["50 per day", "50 per hour"]
)
