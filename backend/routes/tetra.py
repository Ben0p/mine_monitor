
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

    def get(self,):

        node_names = []
        node_loads = []
        node_colors = []

        # Initilize request parser
        parser = reqparse.RequestParser()

        # Execute MySQL query
        CURSOR.execute("SELECT \
            Description, \
            RadioTsCountIdle, \
            RadioTsCountTotal \
            FROM `nodestatus` \
            WHERE StdBy = '0' \
            AND Description NOT LIKE 'ELI%';"
        )

        myresult = CURSOR.fetchall()

        for x in myresult:

            ts_used = int(x[2] or 0) - int(x[1] or 0)

            try:
                load = ts_used / int(x[2] or 0) * 100
            except ZeroDivisionError:
                load = 0
            
            if load >= 90:
                color = 'danger'
            elif 90 > load >= 75:
                color = 'warning'
            elif 75 > load >= 0:
                color = 'success'

            node_names.append(x[0])
            node_loads.append(round(load))
            node_colors.append(color)

        node_load = {
            'node_names' : node_names,
            'node_loads' : node_loads,
            'node_colors' : node_colors
        }


        return(jsonify(json.loads(dumps(node_load))))