from flask import Flask
from werkzeug.contrib.fixers import ProxyFix

from endpoint import api

#last work here, how to import this to user.py ?

from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)

app = Flask(__name__)

# Setup the Flask-JWT-Extended extension
app.config['RESTPLUS_MASK_SWAGGER'] = False # remove default X-Fields field in swagger
app.config['JWT_SECRET_KEY'] = 'super-secret'  # Change this!
jwt = JWTManager(app)

app.wsgi_app = ProxyFix(app.wsgi_app)

api.init_app(app)

app.run(debug=True)