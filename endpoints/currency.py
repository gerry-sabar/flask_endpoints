from flask_restplus import Namespace, Resource, fields

api = Namespace('currencies', description='Currencies related operations')

currency = api.model('Currency', {
    'id': fields.String(required=True, description='The currency identifier'),
    'name': fields.String(required=True, description='The currency name'),
    'rate': fields.Float(required=True, description='The currency rate'),
})

CURRENCIES = [
    {'id': '1', 'name': 'USD', 'rate': 1},
]


@api.route('/')
class CurrencyList(Resource):
    @api.doc('list_currencies')
    @api.marshal_list_with(currency)
    def get(self):
        '''List all currencies'''
        return CURRENCIES


@api.route('/<id>')
@api.param('id', 'The currency identifier')
@api.response(404, 'Currency not found')
class Currency(Resource):
    @api.doc('get_currency')
    @api.marshal_with(currency)
    def get(self, id):
        '''Fetch a currency given its identifier'''
        for currency in CURRENCIES:
            if currency['id'] == id:
                return currency
        api.abort(404)