from flask import Flask
from flask_migrate import Migrate
from sqlalchemy import (Text, String, DateTime)
from datetime import datetime
import uuid
from flask_bcrypt import Bcrypt
git from app import db #this doesn't work!

app = Flask(__name__)
bcrypt = Bcrypt(app)

migrate = Migrate(app, db)

class UserApi(db.Model):
    __tablename__ = 'user'     

    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(String(255))
    email = db.Column(String(255))
    password = db.Column(String(255))
    access_token = db.Column(Text)
    refresh_token = db.Column(Text)
    created_at = db.Column(DateTime)

    @classmethod
    def seed(self, fake):
        user = UserApi(
            uuid = str(uuid.uuid4()),
            email = fake.email(),            
            password = bcrypt.generate_password_hash('password'),
            created_at = datetime.now(),
        )
        db.session.add(user)
        db.session.commit()