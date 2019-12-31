from flask_restplus import Namespace, Resource, fields
from flask_jwt_extended import (
    create_access_token, jwt_required, create_refresh_token, 
    jwt_refresh_token_required, get_jwt_identity, get_raw_jwt,
)
import datetime
from flask import request
from flask_bcrypt import Bcrypt
from app import app,db
from flask_restplus import Resource, fields
from faker import Faker
from models.user import UserApi

api = Namespace('users', description='Users related operations')
user = api.model('UserApi', {
    'uuid': fields.String(required=True, description='User uuid'),
    'email': fields.String(required=True, description='User email'),
    'access_token': fields.String(required=True, description='User access token'),
    'refresh_token': fields.String(required=True, description='User refresh token'),
})

blacklist = set()
bcrypt = Bcrypt(app)

@api.route('/')
class UserList(Resource):
    @jwt_required
    @api.doc('list_users')
    @api.marshal_list_with(user)
    def get(self):
        '''Get all users'''
        users = UserApi.query.all()
        return users

resource_fields = api.model('Login', {
    'email': fields.String,
    'password': fields.String,
})
@api.route('/login')
@api.response(404, 'User not found')
class Login(Resource):
    @api.expect(resource_fields)
    @api.marshal_with(user)
    def post(self):
        """
        Obtain user details & token
        """        
        payload = request.get_json()        
        user = UserApi.query.filter_by(email=payload['email']).first()

        if not user:
            return { 'status': 'invalid username/password'}

        if bcrypt.check_password_hash(user.password, payload['password']):
            expires = datetime.timedelta(minutes=10)
            access_token = create_access_token(identity=payload['email'], fresh=True, expires_delta=expires)
            refresh_token = create_refresh_token(identity=payload['email'])
            user.access_token = access_token
            user.refresh_token = refresh_token
            db.session.add(user)
            db.session.commit()

            return user
        else:
            return { 'status': 'invalid username/password'}

resource_fields = api.model('Refresh', {
    'refresh_token': fields.String,
})
@api.route('/refresh')
@api.response(404, 'Invalid token')
class RefreshToken(Resource):
    @jwt_refresh_token_required
    @api.marshal_with(user)
    def post(self):
        email = get_jwt_identity()

        if not email:
            return { 'status': 'invalid refresh token'}

        jti = get_raw_jwt()['jti']
        blacklist.add(jti)

        user = UserApi.query.filter_by(email=email).first()
        expires = datetime.timedelta(minutes=10)
        user.access_token = create_access_token(identity=email, fresh=True, expires_delta=expires)
        user.refresh_token = create_refresh_token(identity=email)
        return user


update_fields = api.model('Login', {
    'email': fields.String,
})
@api.route('/<uuid>')
@api.param('uuid', 'User UUID')
@api.response(404, 'User not found')
class User(Resource):
    @api.doc('get_user')
    @api.marshal_with(user)
    def get(self, uuid):
        '''Fetch a user given its UUID'''
        user = UserApi.query.filter_by(uuid=uuid).first()

        if not user:
            return { 'status': 'user is not found'}

        return user

    @api.expect(update_fields)
    @api.marshal_with(user)
    def put(self, uuid):
        user = UserApi.query.filter_by(uuid=uuid).first()

        if not user:
            return { 'status': 'user is not found'}

        payload = request.get_json()
        db.session.query(UserApi).filter_by(uuid=uuid).update(payload)
        db.session.commit()

        return user

    def delete(self, uuid):
        user = UserApi.query.filter_by(uuid=uuid).first()

        if not user:
            return { 'status': 'user is not found'}
        db.session.delete(user)
        db.session.commit()
        return ('', 204)
