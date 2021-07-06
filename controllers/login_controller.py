import flask_login
from minimal import sfa_app # importanto a API inteira
from validator_collection import validators, checkers, errors

login_manager = flask_login.LoginManager() # será usado como decorador para controlar o login
APP, SFA = sfa_app.app,sfa_app.api

login_manager.init_app(APP)


# Validation tests
email_address = validators.email('test@domain.dev')
# The value of email_address will now be "test@domain.dev"

try:
    email_address = validators.email(None)
    # Will raise an EmptyValueError
except errors.EmptyValueError:
    # Handling logic goes here
except errors.InvalidEmailError:
    # More handlign logic goes here

email_address = validators.email(None, allow_empty = True)
# The value of email_address will now be None

email_address = validators.email('', allow_empty = True)
# The value of email_address will now be None

is_email_address = checkers.is_email('test@domain.dev')
# The value of is_email_address will now be True

is_email_address = checkers.is_email('this-is-an-invalid-email')
# The value of is_email_address will now be False

is_email_address = checkers.is_email(None)
# The value of is_email_address will now be False




class User(flask_login.UserMixin): # This provides default implementations for the methods that Flask-Login expects user objects to have.
    pass


@login_manager.user_loader # está avisando q a função abaixo tem q retornar um objeto usuário
def user_loader(credentials):

    # {"email":"user@mail.com","password":"123456"}
    if email not in users:
        return

    user = User()
    user.id = email
    return user

@login_manager.request_loader
def request_loader(request):
    email = request.form.get('email')
    if email not in users:
        return

    user = User()
    user.id = email

    # DO NOT ever store passwords in plaintext and always compare password
    # hashes using constant-time comparison!
    user.is_authenticated = request.form['password'] == users[email]['password']

    return user

