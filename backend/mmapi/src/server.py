#! /usr/bin/python3.7

from env.sol import env

from flask import Flask, jsonify, send_file, Response, make_response
from flask_restful import Api, Resource, reqparse
from flask_cors import CORS

import pymongo
from bson.json_util import dumps
from bson.objectid import ObjectId
import json
import copy
import jwt
import datetime

from routes.wind import wind_collect, wind_all, wind_minute, wind_hour, wind_info
from routes.alerts import alert_all, alert_display, alert_detail, alert_overview, alert_modules, alert_zones, alert_zones_create, \
    alert_zones_update, alert_zones_delete, alert_zones_list, alert_types, alert_status, alert_create, alert_update, alert_delete, \
    alert_wz
from routes.auth import auth
from routes.tetra import tetra_node_all, tetra_node_load, tetra_node_subscribers, tetra_ts_load, tetra_radio_count, tetra_subscribers, tetra_call_stats, \
    tetra_call_history, tetra_subscriber_detail, tetra_subscriber_update
from routes.solar import solar_create, solar_update, solar_delete, solar_controllers, solar_data
from routes.gen import gen_create, gen_update, gen_delete, gen_modules, gen_status
from routes.dash import dash_power
from routes.fm import fm_live, fm_modules, fm_create, fm_update, fm_delete
from routes.map import test_czml, test_tetra, tetra_all, map_layers, map_sds, map_sds_range
from routes.ups import ups_create, ups_update, ups_delete, ups_modules, ups_status

""" Main rest API router
"""

# Initialize flask
app = Flask(__name__)
API = Api(app)
CORS(app)

# Initialize mongo connection one time
CLIENT = pymongo.MongoClient('mongodb://{}:{}/'.format(env['mongodb_ip'], env['mongodb_port']))
DB = CLIENT[env['database']]


class check(Resource):
    def get(self):

        response = {'online': True}

        # Return response
        return(jsonify(json.loads(dumps(response))))


# Map URL's to resource classes
# Dashboards
API.add_resource(dash_power, "/api/dash/power")

# Alerts
API.add_resource(alert_all, "/api/alerts/all")
API.add_resource(alert_display, "/api/alerts/display")
API.add_resource(alert_modules, "/api/alerts/modules")
API.add_resource(alert_overview, "/api/alerts/overview")
API.add_resource(alert_zones, "/api/alerts/zones")
API.add_resource(alert_zones_list, "/api/alerts/zones/list")
API.add_resource(alert_zones_create, "/api/alerts/zones/create")
API.add_resource(alert_zones_update, "/api/alerts/zones/update")
API.add_resource(alert_zones_delete, "/api/alerts/zones/delete")
API.add_resource(alert_types, "/api/alerts/types")
API.add_resource(alert_status, "/api/alerts/status")
API.add_resource(alert_create, "/api/alerts/create")
API.add_resource(alert_update, "/api/alerts/update")
API.add_resource(alert_delete, "/api/alerts/delete/<string:name>")
API.add_resource(alert_detail, "/api/alerts/<string:uid>")
API.add_resource(alert_wz, "/api/alerts/wz")
API.add_resource(check, "/api/check")
API.add_resource(auth, "/api/auth")

# Wind
API.add_resource(wind_collect, '/api/wind/<string:name>')
API.add_resource(wind_all, '/api/wind/all')
API.add_resource(wind_minute, '/api/wind/minute/<string:name>/<string:units>')
API.add_resource(wind_hour, '/api/wind/hour/<string:name>/<string:units>')
API.add_resource(wind_info, '/api/wind/info/<string:name>')

# Tetra
API.add_resource(tetra_node_all, '/api/tetra/node/all')
API.add_resource(tetra_node_load, '/api/tetra/node/load')
API.add_resource(tetra_node_subscribers, '/api/tetra/node/subscribers')
API.add_resource(tetra_ts_load, '/api/tetra/ts/load')
API.add_resource(tetra_radio_count, '/api/tetra/radio/count/<string:node>')
API.add_resource(tetra_subscribers, '/api/tetra/subscribers')
API.add_resource(tetra_call_stats, '/api/tetra/callstats/<string:call_type>/<int:range_sec>')
API.add_resource(tetra_call_history, '/api/tetra/callstats/history/<string:time_range>')
API.add_resource(tetra_subscriber_detail, '/api/tetra/subscribers/detail/<string:issi>')
API.add_resource(tetra_subscriber_update, '/api/tetra/subscribers/update')

# Solar
API.add_resource(solar_create, "/api/solar/create")
API.add_resource(solar_update, "/api/solar/update")
API.add_resource(solar_delete, "/api/solar/delete/<string:oid>")
API.add_resource(solar_controllers, '/api/solar/controllers')
API.add_resource(solar_data, '/api/solar/data')

# Generators
API.add_resource(gen_create, "/api/gen/create")
API.add_resource(gen_update, "/api/gen/update")
API.add_resource(gen_delete, "/api/gen/delete/<string:oid>")
API.add_resource(gen_modules, '/api/gen/modules')
API.add_resource(gen_status, '/api/gen/status')

# FM
API.add_resource(fm_live, "/api/fm/live")
API.add_resource(fm_modules, "/api/fm/modules")
API.add_resource(fm_create, "/api/fm/create")
API.add_resource(fm_update, "/api/fm/update")
API.add_resource(fm_delete, "/api/fm/delete/<string:oid>")

# Map
API.add_resource(test_czml, "/api/map/test")
API.add_resource(test_tetra, "/api/map/test_tetra")
API.add_resource(tetra_all, "/api/map/tetra_all")
API.add_resource(map_layers, "/api/map/layers")
API.add_resource(map_sds, "/api/map/sds")
API.add_resource(map_sds_range, "/api/map/sds/range/<string:range>")

# UPS
API.add_resource(ups_create, "/api/ups/create")
API.add_resource(ups_update, "/api/ups/update")
API.add_resource(ups_delete, "/api/ups/delete/<string:oid>")
API.add_resource(ups_modules, '/api/ups/modules')
API.add_resource(ups_status, '/api/ups/status')



if __name__ == "__main__":
    # Run flask
    app.run(debug=True, host='0.0.0.0', port=5000)
