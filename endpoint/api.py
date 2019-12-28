from flask import Flask, request
from flask_restplus import Api, Resource, fields
from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields as FM
from sqlalchemy import (Text)  # you can add another table column type if you need
from flask_migrate import Migrate

from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)

app = Flask(__name__)

# Setup the Flask-JWT-Extended extension
app.config['JWT_SECRET_KEY'] = 'super-secret'  # Change this!
jwt = JWTManager(app)


#add api key
authorizations = {
    'apikey' : {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization'
    }
}

api = Api(app, 
    version='1.0', 
    title='Sample API',
    description='A sample API',
    authorizations=authorizations,
)

name_space = api.namespace('api', description='API Project')
name_space2 = api.namespace('user', description='API User')

# configure SQLAlchemy
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# my MySQL user is root with password root and my database is my_project
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost/flask'
db = SQLAlchemy(app)


# model to table Log
class Log(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    detail = db.Column(Text)


# will be used to serialize model Log into JSON for API result
class LogSchema(Schema):
    id = FM.Int()
    detail = FM.Str()


# this will be used to add parameter in swagger for inserting/updating record
logSwagger = api.model('Log', {
    'detail': fields.String(required=True, description='Log detail content')
})

schema = LogSchema()

# Protect a view with jwt_required, which requires a valid access token
# in the request to access.
@name_space2.route("/protected")
#@jwt_required
class UserDetail(Resource):
    def get(self):
        # Access the identity of the current user with get_jwt_identity
        #current_user = get_jwt_identity()

        return {
            "data": "testign"
        }


@name_space.route("/")
class LogList(Resource):
    # you can add additional Swagger response information here
    @api.doc(
        responses=
        {
            200: 'OK',
            400: 'Invalid Argument',
            500: 'Mapping Key Error',
        })
    def get(self):
        logs = Log.query.all()
        result = []
        schema = LogSchema()
        for log in logs:
            result.append(schema.dump(log))
        return {
            "data": result
        }

    @name_space.expect(logSwagger)
    def post(self):
        payload = request.get_json()
        log = Log()
        log.detail = payload['detail']
        db.session.add(log)
        db.session.commit()

        return {
            "data": schema.dump(log)
        }


@name_space.route("/<int:id>")
#@api.doc(security='apikey'), in case you only have some endpoints that are protected.
class LogDetail(Resource):
    @api.doc(
        responses=
        {
            200: 'OK',
            400: 'Invalid Argument',
            500: 'Mapping Key Error'
        },
        params=
        {
            'id': 'Id log to get the detail'
        })
    def get(self, id):
        log = Log.query.get(id)
        return {
            "data": schema.dump(log)
        }

    @api.doc(
        responses=
        {
            200: 'OK',
            400: 'Invalid Argument',
            500: 'Mapping Key Error'
        },
        params=
        {
            'id': 'Id log to be updated'
        })
    @name_space.expect(logSwagger)
    def put(self, id):
        payload = request.get_json()
        log = Log.query.get(id)
        log.detail = payload['detail']
        db.session.add(log)
        db.session.commit()
        return {
            "data": schema.dump(log)
        }

    @api.doc(
        responses=
        {
            200: 'OK',
            400: 'Invalid Argument',
            500: 'Mapping Key Error'
        },
        params=
        {
            'id': 'Id log to be removed'
        })
    def delete(self, id):
        log = Log.query.get(id)
        db.session.delete(log)
        db.session.commit()
        return {
            "status": "OK"
        }