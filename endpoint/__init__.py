from flask_restplus import Api

from .user import api as user_api
from .currency import api as currency_api

#add api key
authorizations = {
    'apikey' : {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization'
    }
}

api = Api(
    title='Simple API',
    version='1.0',
    description='A simple demo API',
    authorizations=authorizations,
    security='apikey'
)

api.add_namespace(user_api)
api.add_namespace(currency_api)