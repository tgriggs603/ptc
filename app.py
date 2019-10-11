# Python Tech Challenge code

from flask import Flask
from flask_restplus import Api, Resource, reqparse
import dns.resolver
import json


flask_app = Flask(__name__)
api = Api(app=flask_app, version='1.0', title='MX Record API', description='Tech Challenge MX Record API', doc='/docs')
ns = api.namespace('mxrecords', description='MX Record APIs')
not_implemented_exception_json = json.loads(json.dumps({'exception':'Not Implemented'}))


@ns.route('/<string:domain_name>')
@ns.param('domain_name', 'The domain name')
class MXRecordList(Resource):
    def get(self, domain_name):
        try:
            answers = dns.resolver.query(domain_name,'MX')
        except dns.resolver.NXDOMAIN:
            return json.loads(json.dumps({'exception':'NXDOMAIN Exception -- mx record not found'})), 500
        except dns.resolver.Timeout:
            return json.loads(json.dumps({'exception':'Timeout -- mx record not found'})), 500
        except dns.resolver.NoAnswer:
            return json.loads(json.dumps({'exception':'NoAnswer -- mx record not found'})), 500
        else:
            if len(answers) <= 0:
                return json.loads(json.dumps({'exception':'mx record not found'})), 404
            else:
                return_json = json.loads(json.dumps({'records':[]}))
                
            for rdata in answers:
                record_preference = str(rdata).split(' ')[0]
                record_exchange = str(rdata).split(' ')[1]
                return_json['records'].append({'preference': record_preference, 'exchange':record_exchange}) 

        return return_json

@ns.route('/')
@ns.param('domain_name', 'The domain name')
@ns.param('exchange', 'The mx record exchange value')
@ns.param('preference', 'The mx record preference value')
class MXRecord(Resource):
    def post(self):
        return not_implemented_exception_json, 400

    def put(self):
        return not_implemented_exception_json, 400

    def delete(self):
        return not_implemented_exception_json, 400

if __name__ == '__main__':
    flask_app.run(debug=True, host='0.0.0.0')
