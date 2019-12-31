from flask import Flask
from werkzeug.contrib.fixers import ProxyFix
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from flask_jwt_extended import (
    JWTManager,
)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost/flask-restplus'
db = SQLAlchemy(app)
db.init_app(app)

bcrypt = Bcrypt(app)
migrate = Migrate(app, db)
from endpoints import api

# Setup the Flask-JWT-Extended extension
app.config['RESTPLUS_MASK_SWAGGER'] = False # remove default X-Fields field in swagger
app.config['JWT_SECRET_KEY'] = 'super-secret'  # Change this!
jwt = JWTManager(app)

app.wsgi_app = ProxyFix(app.wsgi_app)

api.init_app(app)

app.run(debug=True)

@app.cli.command("seeder")
def seed():
    from faker import Faker
    from models.user import UserApi

    fake = Faker()
    for x in range(3):
        UserApi.seed(fake)