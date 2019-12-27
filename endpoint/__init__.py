from flask_restplus import Api

from .user import api as user_api
from .currency import api as currency_api

api = Api(
    title='Simple API',
    version='1.0',
    description='A simple demo API',
)

api.add_namespace(user_api)
api.add_namespace(currency_api)