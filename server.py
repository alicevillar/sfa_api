from controllers.picture_controller import *
#from controllers.picture_controller_apod import *
from controllers.users_controller import *
from controllers.demo_key_controller import *
from controllers.gdpr_controller import *
from minimal import sfa_app

sfa_app.run()

#####################################################################################################################
#
#   ====>>>> INSTRUCTIONS TO RUN THE MONOLITH AND THE MICROSERVICE:
#
#####################################################################################################################

# ====> To run the monolith:
# a) Containers: the two constainers must be running
# b) Importing: USE ONLY: from controllers.picture_controller import * (NOT the folling: from controllers.picture_controller_apod import *)

# ====> To run the monolith:
# a) Containers: disable container 2 (container with the API)
# b) Importing: USE ONLY the following import: from controllers.picture_controller_apod import *
#-  and invert the import
