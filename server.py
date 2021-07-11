from controllers.picture_controller import *
from controllers.users_controller import *
from controllers.demo_key_controller import *
#from controllers.login_controller import *
from controllers.gdpr_controller import *
from minimal import sfa_app


sfa_app.run()

#####################################################################################################################
#
#                                         MCV - Model-View-Controller
#
#   MVC is a software design pattern for user interfaces that divides the program into three elements:
#   MVC includes the model (data), the view (user interface), and the controller (processes that handle input)
#
#   ==> SFA - MVC:
#
#   M => The type of data we are using in the application: user's data and picture data (json)
#   V => Our interface (Html/CSS/Javascript) and Swagger
#   C => It is in the file with 6 controllers (picture controller and user controller)
#
#####################################################################################################################

