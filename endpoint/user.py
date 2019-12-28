from flask_restplus import Namespace, Resource, fields
from flask_jwt_extended import (
    create_access_token, jwt_required, create_refresh_token, 
    jwt_refresh_token_required
)
import datetime

api = Namespace('users', description='Users related operations')

user = api.model('User', {
    'id': fields.String(required=True, description='The user id'),
    'email': fields.String(required=True, description='The user email'),
})

USERS = [
    {'id': '1', 'email': 'example@example.com'},
]


@api.route('/')
class UserList(Resource):
    @jwt_required
    @api.doc('list_users')
    @api.marshal_list_with(user)
    def get(self):
        '''List all users'''
        return USERS

@api.route('/token/<id>')
@api.param('id', 'The user identifier')
@api.response(404, 'User not found')
class UserToken(Resource):
    def get(self, id):
        for user in USERS:
            if user['id'] == id:
                expires = datetime.timedelta(minutes=10)
                access_token = create_access_token(identity=user['email'], fresh=True, expires_delta=expires)
                refresh_token = create_refresh_token(identity=user['email'])                
                return {'token': access_token, 'refresh_token': refresh_token}, 200        
        api.abort(404)    

@api.route('/refresh/<refresh_token>')
@api.param('refresh_token', 'Valid refresh token')
@api.response(404, 'Invalid token')
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
    @api.marshal_with(user)
    def get(self, id):
        '''Fetch a user given its identifier'''
        for user in USERS:
            if user['id'] == id:
                return user
        api.abort(404)