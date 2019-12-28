from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import (Text, String, DateTime)
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import uuid

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost/flask-restplus'

db = SQLAlchemy(app)
migrate = Migrate(app, db)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(String(255))
    email = db.Column(String(255))
    password = db.Column(String(255))
    access_token = db.Column(Text)
    refresh_token = db.Column(Text)
    created_at = db.Column(DateTime)

    @classmethod
    def seed(self, fake):
        user = User(
            uuid = str(uuid.uuid4()),
            email = fake.email(),
            password = generate_password_hash('password'),
            created_at = datetime.now(),
        )
        db.session.add(user)
        db.session.commit()
