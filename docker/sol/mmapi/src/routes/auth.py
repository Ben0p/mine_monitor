from env.sol import env

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
            'authenticated' : True,
            'connected' : True,
            'alert_read' : True,
            'alert_admin' : True,
        }

        # Initilize request parser
        parser = reqparse.RequestParser()

        # Parse arguments from form data
        parser.add_argument("email")
        parser.add_argument("password")

        args = parser.parse_args()

        result['description'] = 'Kicking Goals'
        result['display_name'] = 'Mine Services'
        result['role'] = 'alert_admin'

        token = jwt.encode(result, args['password'], algorithm='HS256')
        response = {'token' : token.decode("utf-8")}

        return(jsonify(json.loads(dumps(response))))