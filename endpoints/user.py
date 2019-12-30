from flask import Flask, session
from flask_restplus import Namespace, Resource, fields
from flask_jwt_extended import (
    create_access_token, jwt_required, create_refresh_token, 
    jwt_refresh_token_required
)
import datetime
from flask import request
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

import sys
sys.path.append("..")
from models.user import UserApi

api = Namespace('users', description='Users related operations')

USERS = [
    {'id': '1', 'email': 'example@example.com'},
]

app = Flask(__name__)
bcrypt = Bcrypt(app)
db = SQLAlchemy(app)
db.init_app(app)


@api.route('/')
class UserList(Resource):
    @jwt_required
    @api.doc('list_users')
    #@api.marshal_list_with(user)
    def get(self):
        '''description goes here...'''
        return USERS

resource_fields = api.model('User', {
    'email': fields.String,
    'password': fields.String,
})
@api.route('/login')
@api.response(404, 'User not found')
class Login(Resource):
    @api.expect(resource_fields)
    def post(self):
        """
        Obtain user details & token
        """        
        payload = request.get_json()        
        user = UserApi.query.filter_by(email='joshua72@wilson.com').first()

        if not user:
            return { 'status': 'invalid username/password'}

        if bcrypt.check_password_hash(user.password, 'password'):
            expires = datetime.timedelta(minutes=10)
            access_token = create_access_token(identity=user.email, fresh=True, expires_delta=expires)
            refresh_token = create_refresh_token(identity=user.email)                
            user.access_token = access_token
            user.refresh_token = refresh_token
            #userSession = db.session.merge(user)
            db.session.add(user)
            db.session.commit()            
            db.session.close()
            return {
                'uuid': user.uuid,
                'email': user.email,
                'access_token': user.access_token,
                'refresh_token': user.refresh_token,
            }
        else:
            return { 'status': 'invalid username/password'}
        #return payload['name']


@api.route('/refresh/<refresh_token>')
@api.param('refresh_token', 'Valid refresh token')
@api.response(404, 'Invalid token')
@api.doc(params={'id': 'example of additional optional parameter'})
class RefreshToken(Resource):
    @jwt_refresh_token_required
    def get(self, refresh_token):
        expires = datetime.timedelta(minutes=10)
        access_token = create_access_token(identity=USERS[0]['email'], fresh=True, expires_delta=expires)
        refresh_token = create_refresh_token(identity=USERS[0]['email'])                
        return {'token': access_token, 'refresh_token': refresh_token}, 200        


@api.route('/<id>')
@api.param('id', 'The user identifier')
@api.response(404, 'User not found')
#@api.doc(security='apikey'), in case you only have some endpoints that are protected.
class User(Resource):
    @api.doc('get_user')
    #@api.marshal_with(user)
    def get(self, id):
        '''Fetch a user given its identifier'''
        for user in USERS:
            if user['id'] == id:
                return user
        api.abort(404)