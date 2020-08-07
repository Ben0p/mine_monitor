
from env.sol import env

from flask_restful import Resource, reqparse
import pymongo
from bson.json_util import dumps
from bson.objectid import ObjectId
import json
from json import JSONEncoder
import copy
import time
from flask import jsonify, request, Response
import datetime
import mysql.connector



# Initialize mongo connection one time
CLIENT = pymongo.MongoClient(f"mongodb://{env['mongodb_ip']}:{env['mongodb_port']}/")
DB = CLIENT[env['database']]



class test_czml(Resource):

    def get(self):
        # test data

        """
        czml = [
            {
                'id': "document",
                'name': "CZML Point - Time Dynamic",
                'version': "1.0",
            },
            {
                'id': "point",
                'availability': "2020-06-22T00:00:00Z/2020-06-22T00:05:00Z",
                'position': {
                    'epoch': "2020-06-22T00:00:00Z",
                    'cartographicDegrees': [
                    0, -70, 20,150000,
                    100, -80, 44, 150000,
                    200, -90, 18, 150000,
                    300, -98, 52, 150000,
                    ],
                },
                'point': {
                    'color': {
                    'rgba': [255, 255, 255, 128],
                    },
                    'outlineColor': {
                    'rgba': [255, 0, 0, 128],
                    },
                    'outlineWidth': 3,
                    'pixelSize': 15,
                },
            },
        ]
        """


        # First packet id NEEDS to be "document"
        czml = [
            {
                'id': "document",
                'name': "Tetra CZML data",
                'version': "1.0",
            },
            {
                'id': "Test CZML 01",
                'availability': "2012-04-30T12:00Z/2012-04-30T12:03Z",
                'position': {
                    'cartographicDegrees': [
                        '2012-04-30T12:00Z', -70, 20, 150000,
                        '2012-04-30T12:01Z', -80, 44, 150000,
                        '2012-04-30T12:02Z', -90, 18, 150000,
                        '2012-04-30T12:03Z', -98, 52, 150000,
                    ],
                },
                'point': {
                    'color': {
                    'rgba': [255, 255, 255, 128],
                    },
                    'outlineColor': {
                    'rgba': [255, 0, 0, 128],
                    },
                    'outlineWidth': 3,
                    'pixelSize': 15,
                },
            },
            {
                'id': "Test CZML 02",
                'position': {
                    'cartographicDegrees': [
                        '2012-04-30T12:00Z', -72, 22, 150000,
                        '2012-04-30T12:01Z', -82, 46, 150000,
                        '2012-04-30T12:02Z', -92, 20, 150000,
                        '2012-04-30T12:03Z', -100, 54, 150000,
                    ],
                },
                'point': {
                    'color': {
                    'rgba': [255, 255, 255, 128],
                    },
                    'outlineColor': {
                    'rgba': [255, 0, 0, 128],
                    },
                    'outlineWidth': 3,
                    'pixelSize': 15,
                },
            },
        ]



        return(jsonify(json.loads(dumps(czml))))


class test_tetra(Resource):

    def get(self):

        points = DB['map_tetra'].find(
            {
                'unix' : {
                    '$gte' : time.time() - 60
                }
            },
        )

        # First packet id NEEDS to be "document"
        czml = [
            {
                'id': "document",
                'name': "Tetra CZML data",
                'version': "1.0",
            }
        ]

        for point in points:

            description = "LIVE INFORMATION<br>" \
                          f"&nbsp;&nbsp;ISSI: {point['issi']}<br>"\
                          f"&nbsp;&nbsp;Node: {point['node']}<br>"\
                          f"&nbsp;&nbsp;Group: {point['talkgroup']}<br>"\
                          f"&nbsp;&nbsp;Speed: {point['velocity']}kmh - {point['direction']}<br>"\
                          f"&nbsp;&nbsp;RSSI: {point['rssi']}dBm<br>"\
                          f"&nbsp;&nbsp;Accuracy: {point['uncertainty']}m"

            czml.append(
                {
                    'id': point['issi'],
                    'name' : point['description'],
                    'description' : description,
                    'availability' : f"{point['availability_start']}/{point['availability_end']}",
                    'position': {
                        'cartesian': point['point'],
                    },
                    'point': {
                        'color': {
                            'interval' : f"{point['properties_start']}/{point['properties_end']}",
                            'rgba': point['rssi_color'],
                        },
                        'outlineColor': {
                            'interval' : f"{point['properties_start']}/{point['properties_end']}",
                            'rgba': point['velocity_color'],
                        },
                        'outlineWidth': 3,
                        'pixelSize': 15,
                        "heightReference" : "CLAMP_TO_GROUND",
                    },
                    'label' : {
                        'show' : False,
                        'fillColor': {
                            'rgba': [255, 255, 255, 255],
                        },
                        'font': "12pt Lucida Console",
                        'horizontalOrigin': "LEFT",
                        'pixelOffset': {
                            'cartesian2': [8, 0],
                        },
                        'style': "FILL",
                        'text': f"{point['velocity']} kmh",
                        'showBackground': False,
                        'backgroundColor': {
                            'rgba': [112, 89, 57, 200],
                        },
                        "heightReference" : "CLAMP_TO_GROUND",
                    },
                }
            )

        return(jsonify(json.loads(json.dumps(czml))))


class tetra_all(Resource):
    def get(self):

        points = DB['map_tetra'].find()


        # First packet id NEEDS to be "document"
        czml = [
            {
                'id': "document",
                'name': "Tetra CZML data",
                'version': "1.0",
            }
        ]

        for point in points:

            czml.append(
                {
                    'id': point['issi'],
                    'position': {
                        'cartesian': point['point'],
                    },
                    'point': {
                        'color': {
                            'rgba': [255, 255, 255, 128],
                        },
                        'outlineColor': {
                            'rgba': [255, 0, 0, 128],
                        },
                        'outlineWidth': 3,
                        'pixelSize': 15,
                        "heightReference" : "CLAMP_TO_GROUND",
                    },
                }
            )

        return(jsonify(json.loads(json.dumps(czml))))


class map_layers(Resource):

    def get(self):
        # Get list of layers
        map_layers = DB['map_layers'].find()
        
        return(jsonify(json.loads(dumps(map_layers))))


class map_sds(Resource):

    def get(self):

        points = DB['sds_data'].find(
            {
                'unix' : {
                    '$gte' : time.time() - 60
                }
            },
        )

        # First packet id NEEDS to be "document"
        czml = [
            {
                'id': "document",
                'name': "Tetra CZML data",
                'version': "1.0",
            }
        ]

        for point in points:

            description = "LIVE INFORMATION<br>" \
                          f"&nbsp;&nbsp;ISSI: {point['issi']}<br>"\
                          f"&nbsp;&nbsp;Node: {point['node']}<br>"\
                          f"&nbsp;&nbsp;Group: {point['talkgroup']}<br>"\
                          f"&nbsp;&nbsp;Speed: {point['velocity']}kmh - {point['direction']}<br>"\
                          f"&nbsp;&nbsp;RSSI: {point['rssi']}dBm<br>"\
                          f"&nbsp;&nbsp;Accuracy: {point['uncertainty']}m"

            czml.append(
                {
                    'id': point['issi'],
                    'name' : point['description'],
                    'description' : description,
                    'availability' : f"{point['availability_start']}/{point['availability_end']}",
                    'position': {
                        'cartesian': point['point'],
                    },
                    'point': {
                        'color': {
                            'interval' : f"{point['properties_start']}/{point['properties_end']}",
                            'rgba': point['rssi_color'],
                        },
                        'outlineColor': {
                            'interval' : f"{point['properties_start']}/{point['properties_end']}",
                            'rgba': point['velocity_color'],
                        },
                        'outlineWidth': 3,
                        'pixelSize': 15,
                        "heightReference" : "CLAMP_TO_GROUND",
                    },
                    'label' : {
                        'show' : False,
                        'fillColor': {
                            'rgba': [255, 255, 255, 255],
                        },
                        'font': "12pt Lucida Console",
                        'horizontalOrigin': "LEFT",
                        'pixelOffset': {
                            'cartesian2': [8, 0],
                        },
                        'style': "FILL",
                        'text': f"{point['velocity']} kmh",
                        'showBackground': False,
                        'backgroundColor': {
                            'rgba': [112, 89, 57, 200],
                        },
                        "heightReference" : "CLAMP_TO_GROUND",
                    },
                }
            )

        return(jsonify(json.loads(json.dumps(czml))))