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





# Limiter - Demo key