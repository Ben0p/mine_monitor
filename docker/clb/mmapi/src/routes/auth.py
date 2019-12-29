from env.devprod import env
# from env.docker import env

from env.docker import env
from flask import Flask, jsonify, send_file, Response, make_response
from flask_restful import Api, Resource, reqparse
from pyModbusTCP.client import ModbusClient
from flask_cors import CORS
from ldap3 import Server, Connection, ALL, NTLM, ALL_ATTRIBUTES, ALL_OPERATIONAL_ATTRIBUTES, AUTO_BIND_NO_TLS, SUBTREE, Tls
from ldap3.core.exceptions import LDAPCursorError, LDAPInvalidCredentialsResult, LDAPSocketOpenError, LDAPOperationsErrorResult
import ssl
import pymongo
from bson.json_util import dumps
from bson.objectid import ObjectId
import json
import copy
import jwt
import datetime

class auth(Resource):
    """POST auth"""

    def post(self):
        result = {
            'authenticated' : False,
            'connected' : False,
            'alert_read' : False,
            'alert_admin' : False,
        }

        # Initilize request parser
        parser = reqparse.RequestParser()

        # Parse arguments from form data
        parser.add_argument("email")
        parser.add_argument("password")

        args = parser.parse_args()

        tls_configuration = Tls(validate=ssl.CERT_NONE,
                                version=ssl.PROTOCOL_TLSv1)
        s = Server(f"{env['dc_ip']}", use_ssl=True, tls=tls_configuration)

        try:
            c = Connection(s, user=f"{env['domain']}\\{args['email']}",
                           password=f"{args['password']}", check_names=True, lazy=False, raise_exceptions=True)
            c.open()
            c.bind()
            result['authenticated'] = True
            result['connected'] = True



        except LDAPInvalidCredentialsResult:
            return(make_response(jsonify(result), 404))

        except LDAPSocketOpenError:
            return(make_response(jsonify(result), 404))
    
        except LDAPOperationsErrorResult:
            return(make_response(jsonify(result), 404))

        if result['authenticated']:
            c.search(
                search_base= env['base_ou'],
                search_filter=f"(&(objectclass=person)(sAMAccountName={args['email']}))",
                attributes=[ALL_ATTRIBUTES, ALL_OPERATIONAL_ATTRIBUTES],
                search_scope=SUBTREE,
            )

            for e in c.entries:
                e_json = e.entry_to_json()
                e_dict = json.loads(e_json)
                e_dict = e_dict['attributes']
                for CN in e_dict['memberOf']:
                    CN = CN.split(',')[0]
                    CN = CN.split('=')[1]
                    if CN == env['alert_read']:
                        result['alert_read'] = True
                    if CN == env['alert_admin']:
                        result['alert_admin'] = True

                try:
                    result['mail'] = e_dict['mail'][0]
                except KeyError:
                    result['mail'] = ''
                try:
                    result['description'] = e_dict['description'][0]
                except KeyError:
                    result['description'] = ''
                try:
                    result['display_name'] = e_dict['displayName'][0]
                except KeyError:
                    result['display_name'] = ''
                try:
                    result['given_name'] = e_dict['givenName'][0]
                except KeyError:
                    result['given_name'] = ''
                try:
                    result['username'] = e_dict['sAMAccountName'][0]
                except KeyError:
                    result['username'] = ''
                try:
                    result['last_name'] = e_dict['sn'][0]
                except KeyError:
                    result['last_name'] = ''
                try:
                    result['phone'] = e_dict['telephoneNumber'][0]
                except KeyError:
                    result['phone'] = ''

                    
            if result['alert_admin'] == True:
                result['role'] = 'alert_admin'
            if result['alert_read'] == True and result['alert_admin'] == False:
                result['role'] = 'alert_read'

            token = jwt.encode(result, args['password'], algorithm='HS256')
            response = {'token' : token.decode("utf-8")}

            return(jsonify(json.loads(dumps(response))))