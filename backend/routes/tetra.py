
from env.sol import env

from flask_restful import Resource, reqparse
import pymongo
from bson.json_util import dumps
from bson.objectid import ObjectId
import json
import copy
import time
from flask import jsonify, request
import datetime
import mysql.connector


# Initialize mongo connection one time
CLIENT = pymongo.MongoClient(f"mongodb://{env['mongodb_ip']}:{env['mongodb_port']}/")
DB = CLIENT[env['database']]

# Initialize mySQL connection
SQL = mysql.connector.connect(
  host=f"{env['tetra_sql_host']}",
  user=f"{env['tetra_sql_user']}",
  passwd=f"{env['tetra_sql_passwd']}",
  database=f"{env['tetra_sql_database']}"
)

CURSOR = SQL.cursor()


class tetra_node_all(Resource):

    def get(self,):

        nodes = []

        # Initilize request parser
        parser = reqparse.RequestParser()

        # Execute MySQL query
        CURSOR.execute("SELECT \
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

        myresult = CURSOR.fetchall()

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