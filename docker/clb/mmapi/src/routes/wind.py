from flask_restful import Resource, reqparse

from env.docker import env
import pymongo
from bson.json_util import dumps
from bson.objectid import ObjectId
import json
import copy
import time
from flask import jsonify, request
import datetime

# Initialize mongo connection one time
CLIENT = pymongo.MongoClient(f"mongodb://{env['mongodb_ip']}:{env['mongodb_port']}/")
DB = CLIENT[env['database']]

def windDirection(deg):
    deg = float(deg)
    direction = 'N'
    
    if deg >= 349 and deg <= 11:
        direction = 'N'
    elif deg >= 12 and deg <= 33:
        direction = 'NNE'
    elif deg >= 34 and deg <= 56:
        direction = 'NE'
    elif deg >= 57 and deg <= 78:
        direction = 'ENE'
    elif deg >= 79 and deg <= 101:
        direction = 'E'
    elif deg >= 102 and deg <= 123:
        direction = 'ESE'
    elif deg >= 124 and deg <= 146:
        direction = 'SE'
    elif deg >= 147 and deg <= 168:
        direction = 'SSE'
    elif deg >= 169 and deg <= 191:
        direction = 'S'
    elif deg >= 192 and deg <= 213:
        direction = 'SSW'
    elif deg >= 214 and deg <= 236:
        direction = 'SW'
    elif deg >= 237 and deg <= 258:
        direction = 'WSW'
    elif deg >= 259 and deg <= 281:
        direction = 'W'
    elif deg >= 282 and deg <= 303:
        direction = 'WNW'        
    elif deg >= 304 and deg <= 326:
        direction = 'NW'
    elif deg >= 327 and deg <= 348:
        direction = 'NNW'    

    return(direction)

def windKnots(speed):
    knots = float(speed) * 1.943844
    knots = round(knots, 2)

    return(knots)

def windKmh(speed):
    kmh = float(speed) * 3.6
    kmh = round(kmh, 2)

    return(kmh)

def windHour(name):
    
    current_hour = int(time.strftime('%Y%m%d%H'))
    max_hour = 0

    wind_minute = DB['wind_history'].find_one({'name': name})

    try:
        hours = wind_minute['hour']
    except:
        hours = []
    
    # I ROFLed over this one
    if len(hours) >= 1:
        for hour in hours:
            if hour['hour'] > max_hour:
                max_hour = hour['hour']
    
    eight_hours = time.time() + 28800
    formatted_time = time.strftime('%d/%m/%Y %H00', time.localtime(eight_hours))

    if current_hour > max_hour:

        speeds = [float(minute['ms']) for minute in wind_minute['minute']]
        maximum = max(speeds)
        minimum = min(speeds)
        average = sum(speeds) / len(speeds)
        average = round(average, 2)

        max_kmh = windKmh(maximum)
        max_knots = windKnots(maximum)

        min_kmh = windKmh(minimum)
        min_knots = windKnots(minimum)

        avg_kmh = windKmh(average)
        avg_knots = windKnots(average)

        DB['wind_history'].update(
            {
                'name': name,
            },
            {
                '$push' : {
                    'hour' : {
                        'utc': datetime.datetime.utcnow(),
                        'unix' : time.time(),
                        'time': formatted_time,
                        'hour': current_hour,
                        'ms' : {
                            'max' : maximum,
                            'min' : minimum,
                            'avg' : average
                        },
                        'knots' : {
                            'max' : max_knots,
                            'min' : min_knots,
                            'avg' : avg_knots
                        },
                        'kmh' : {
                            'max' : max_kmh,
                            'min' : min_kmh,
                            'avg' : avg_kmh
                        },
                    },
                },
            },
            upsert = True
        )





class wind_collect(Resource):

    def get(self, name):
        # Initilize request parser
        parser = reqparse.RequestParser()

        # Parse arguments from form data
        parser.add_argument("mac")
        parser.add_argument("name")
        parser.add_argument("directionV")
        parser.add_argument("speedV")
        args = parser.parse_args()

        direction = windDirection(args['directionV'])
        knots = windKnots(args['speedV'])
        kmh = windKmh(args['speedV'])

        eight_hours = time.time() + 28800
        formatted_time = time.strftime('%d/%m/%Y %X', time.localtime(eight_hours))

        DB['wind_live'].find_one_and_update(
            {
                'name':args['name']
            },
            {
                '$set': {
                    'mac' : args['mac'],
                    'ip': request.remote_addr,
                    'name' : args['name'],
                    'degrees' : args['directionV'],
                    'direction' : direction,
                    'ms' : args['speedV'],
                    'knots' : knots,
                    'kmh' : kmh,
                }
            },
            upsert=True
        )

        DB['wind_history'].update(
            {
                'name':args['name'],
            },
            {
                '$push' : {
                    'minute' : {
                        'utc': datetime.datetime.utcnow(),
                        'unix' : time.time(),
                        'time': formatted_time,
                        'degrees' : args['directionV'],
                        'direction' : direction,
                        'ms' : args['speedV'],
                        'knots' : knots,
                        'kmh' : kmh,
                    },
                },
            },
            upsert = True
        )

        DB['wind_history'].update(
            {
                'name': args['name'],
            },
            {
                '$pull' : {
                    'minute' : {
                        'unix' : { 
                            '$lte': time.time() - 3600 # 1 hour
                        },
                    },
                    'hours' : {
                        'unix' : { 
                            '$lte': time.time() - 172800 # 48 hours
                        }
                    }
                }
            },
        )

        windHour(args['name'])


class wind_all(Resource):

    def get(self):

        winds = DB['wind_live'].find().sort("name", pymongo.ASCENDING)

        return(jsonify(json.loads(dumps(winds))))

class wind_minute(Resource):

    def get(self, name, units):

        speed = DB['wind_history'].find_one(
            {
                'name': name,
            }
        )

        time = [minute['time'] for minute in speed['minute']]
        speed = [minute[units] for minute in speed['minute']]


        result = {
            'name' : name,
            'time'  : time,
            'speed' : speed
        }


        return(jsonify(json.loads(dumps(result))))

class wind_hour(Resource):

    def get(self, name, units):

        time = []

        ms_max = []
        ms_min = []
        ms_avg = []

        kmh_max = []
        kmh_min = []
        kmh_avg = []

        knots_max = []
        knots_min = []
        knots_avg = []

        speed = DB['wind_history'].find_one(
            {
                'name': name,
            }
        )

        if 'hour' in speed:
            for hour in speed['hour']:
                time.append(hour['time'])

                ms_max.append(hour['ms']['max'])
                ms_min.append(hour['ms']['min'])
                ms_avg.append(hour['ms']['avg'])

                kmh_max.append(hour['kmh']['max'])
                kmh_min.append(hour['kmh']['min'])
                kmh_avg.append(hour['kmh']['avg'])

                knots_max.append(hour['knots']['max'])
                knots_min.append(hour['knots']['min'])
                knots_avg.append(hour['knots']['avg'])

            result = {
                'name' : name,
                'time'  : time,
                'ms': {
                    'max' : ms_max,
                    'min' : ms_min,
                    'avg' : ms_avg,
                },
                'kmh' : {
                    'max' : kmh_max,
                    'min' : kmh_min,
                    'avg' : kmh_avg,
                },
                'knots' : {
                    'max' : knots_max,
                    'min' : knots_min,
                    'avg' : knots_avg,
                }
            }

        else:
            result = []


        return(jsonify(json.loads(dumps(result))))

class wind_info(Resource):

    def get(self, name):

        wind = DB['wind_live'].find_one({'name': name})

        return(jsonify(json.loads(dumps(wind))))


