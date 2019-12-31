from flask_restplus import Namespace, Resource, fields
import requests
import json
from flask import request

api = Namespace('currencies', description='Currencies related operations')

@api.route('/')
class CurrencyList(Resource):
    @api.doc('list_currencies')
    @api.param('base', 'base exachange currency')
    def get(self):
        if request.args.get('base') is None:
            base = 'USD'
        else:
            base = request.args.get('base')

        stringRequest = 'https://api.exchangeratesapi.io/latest?base=' + base
        r = requests.get(stringRequest)
        '''List all currencies'''
        json_data = json.loads(r.text)
        return json_data
