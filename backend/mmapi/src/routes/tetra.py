
from env.sol import env

from flask_restful import Resource, reqparse
import pymongo
from bson.json_util import dumps
from bson.objectid import ObjectId
import json
import copy
import time
from flask import jsonify, request, Response
import datetime
import mysql.connector

from tetra.decode import sds



# Initialize mongo connection one time
CLIENT = pymongo.MongoClient(f"mongodb://{env['mongodb_ip']}:{env['mongodb_port']}/")
DB = CLIENT[env['database']]


def reconnectSQL():
    # Initialize mySQL connection
    sql = mysql.connector.connect(
    host=f"{env['tetra_sql_host']}",
    user=f"{env['tetra_sql_user']}",
    passwd=f"{env['tetra_sql_passwd']}",
    database=f"{env['tetra_sql_database']}"
    )

    return(sql)


class tetra_node_all(Resource):

    def get(self,):

        nodes = []

        # Initilize request parser
        parser = reqparse.RequestParser()

        sql = reconnectSQL()
        cursor = sql.cursor()

        # Execute MySQL query
        cursor.execute("SELECT \
            Timestamp, \
            NodeNo, \
            Description, \
            RadioRegMsCount, \
            RadioTsCountIdle, \
            RadioTsCountTotal, \
            RadioTsCountItch, \
            RadioTsCountGtch, \
            RadioTsCountMcch, \
            RadioTsCountScch \
            FROM `nodestatus` \
            WHERE StdBy = '0' \
            AND Description NOT LIKE 'ELI%';"
        )

        myresult = cursor.fetchall()

        for x in myresult:

            ts_used = int(x[5] or 0) - int(x[4] or 0)

            try:
                load = ts_used / int(x[5] or 0) * 100
            except ZeroDivisionError:
                load = 0



            info = {
                'timestamp' : x[0],
                'node_number' : x[1],
                'node_description' : x[2],
                'radio_count' : x[3],
                'ts_idle' : x[4],
                'ts_total' : x[5],
                'ts_in' : x[6],
                'ts_gr' : x[7],
                'ts_mc' : x[8],
                'ts_sc' : x[9],
                'ts_used' : ts_used,
                'load' : round(load)
            } 

            nodes.append(info)


        return(jsonify(json.loads(dumps(nodes))))


class tetra_node_load(Resource):

    def get(self):
        # Get zone list
        node_loads = DB['tetra_node_load'].find_one(
            {
                'type': 'bar'
            }
        )

        return(jsonify(json.loads(dumps(node_loads))))


class tetra_node_subscribers(Resource):

    def get(self):
        # Get zone list
        node_loads = DB['tetra_node_subscribers'].find_one(
            {
                'type': 'bar'
            }
        )

        return(jsonify(json.loads(dumps(node_loads))))


class tetra_ts_load(Resource):

    def get(self):
        # Get zone list
        ts_loads = DB['tetra_node_load'].find_one(
            {
                'type': 'radar'
            }
        )
 
        return(jsonify(json.loads(dumps(ts_loads))))

class tetra_radio_count(Resource):

    def get(self, node):
        # Get zone list
        radio_count = DB['tetra_radio_count'].find_one(
            {
                'node': node
            }
        )
 
        return(jsonify(json.loads(dumps(radio_count))))


class tetra_subscribers(Resource):

    def get(self,):

        # Get subscriber list (all)
        subscribers = DB['tetra_subscribers'].find({}, {'_id': False}).sort("ssi", pymongo.ASCENDING)
 
        return(jsonify(json.loads(dumps(subscribers))))


class tetra_call_stats(Resource):

    def get(self, call_type, range_sec):

        # Get subscriber list (all)
        stats = DB['tetra_call_stats'].find_one(
            {
                'type' : call_type,
                'range_sec' : range_sec
            },
            {'_id': False})
 
        return(jsonify(json.loads(dumps(stats))))

class tetra_call_history(Resource):

    def get(self, time_range):

        # Get subscriber list (all)
        stats = DB['tetra_call_stats'].find_one(
            {
                'type' : 'history',
                'range' : time_range
            },
            {'_id': False})
 
        return(jsonify(json.loads(dumps(stats))))


class tetra_subscriber_detail(Resource):

    def get(self, issi):

        filter={
            'issi': int(issi)
        }
        sort=list({
            'unix': -1
        }.items())
        limit=1

        results = DB['sds_data'].find(
            filter=filter,
            sort=sort,
            limit=limit
        )

        try:
            results = results[0]
            timestamp = str(results['processed_time'] + datetime.timedelta(hours=8))
            lat = results['decimal_degrees']['latitude']
            lon = results['decimal_degrees']['longitude']
            url = f"https://www.google.com/maps/search/?api=1&query={lat},{lon}"

            detail = {
                'timestamp' : timestamp,
                'node' : results['node'],
                'gps' : True,
                'rssi' : results['rssi'],
                'location' : results['decimal_degrees'],
                'maps_url' : url,
                'accuracy' : results['uncertainty'],
                'velocity' : results['velocity'],
                'direction' : results['direction'],
                'angle' : results['angle']
            }
        except IndexError:
            detail = {
                  'gps' : False,
            }

 
        return(jsonify(json.loads(dumps(detail))))


class tetra_subscriber_update(Resource):

    def post(self):

        # Initilize request parser
        parser = reqparse.RequestParser()

        # Parse arguments from form data
        parser.add_argument("ssi")
        parser.add_argument("comment")


        args = parser.parse_args()
        print(args)

        try:
            DB['tetra_subscribers'].find_one_and_update(
                {
                    "ssi": int(args['ssi']),
                },
                {
                    "$set":
                        {
                            "comment": args['comment'],
                        }
                 },
                 upsert=True
            )
            

            return({'success': True, 'message': 'Updated {}'.format(args['ssi'])})

        except Exception as e:
            return({'success': False, 'message': f'{str(e)}'})
