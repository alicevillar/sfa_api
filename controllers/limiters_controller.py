from flask import request
from flask import Flask
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from minimal import sfa_app


# Protecting against DDOs attacks

# Limiter - IP

#################################################################################################################
#   OWASP C7: Enforce Access Controls
#
# In this file you can see the code to monitor the rate limits of both the authentication key and the demo key:
# The requests per IP address have the following limits: 30 per day/30 per hour
#
##################################################################################################################

APP, SFA = sfa_app.app,sfa_app.api

# Defining the limiter
ip_limiter = Limiter(
    APP,
    # This functions returns the IP, so it can recognize when the same IP uses the API more than x times
    key_func=get_remote_address,
    default_limits=["30 per day", "30 per hour"],
    headers_enabled = True
)

# Function to help the limitation library. This function will count the number of requests per key
def get_key():
    try:
        api_key = request.headers['X-API-KEY']
        return api_key

    except: # If the API key hasn't been received, return an error.
        raise Exception('Request done with no API Key. Limiting could not be done')

key_usage_limiter = Limiter(
    APP,
    # This functions returns the IP, so it can recognize when the same IP uses the API more than x times
    key_func=get_key,
    default_limits=["30 per day", "30 per hour"],
    headers_enabled = True
)
