from sqlalchemy import (Text, String, DateTime)
from datetime import datetime
import uuid
from app import db
from app import bcrypt
from werkzeug.security import generate_password_hash, check_password_hash

class UserApi(db.Model):
    __tablename__ = 'user'     

    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(String(255))
    email = db.Column(String(255))
    password_hash = db.Column(String(255))
    access_token = db.Column(Text)
    refresh_token = db.Column(Text)
    created_at = db.Column(DateTime)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    @classmethod
    def seed(self, fake):
        user = UserApi(
            uuid = str(uuid.uuid4()),
            email = fake.email(),            
            password = 'password',
            created_at = datetime.now(),
        )
        db.session.add(user)
        db.session.commit()
