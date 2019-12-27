from flask_restplus import Namespace, Resource, fields

api = Namespace('users', description='Users related operations')

user = api.model('User', {
    'id': fields.String(required=True, description='The user id'),
    'email': fields.String(required=True, description='The user email'),
})

USERS = [
    {'id': '1', 'email': 'example@example.com'},
]


@api.route('/')
class CatList(Resource):
    @api.doc('list_users')
    @api.marshal_list_with(user)
    def get(self):
        '''List all users'''
        return USERS


@api.route('/<id>')
@api.param('id', 'The user identifier')
@api.response(404, 'User not found')
class User(Resource):
    @api.doc('get_user')
    @api.marshal_with(user)
    def get(self, id):
        '''Fetch a user given its identifier'''
        for user in USERS:
            if user['id'] == id:
                return user
        api.abort(404)