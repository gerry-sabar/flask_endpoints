from sqlalchemy import (Text, String, DateTime)
from datetime import datetime
import uuid
from app import db
from app import bcrypt

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