from flask_restful import Resource, reqparse

from env.sol import env

import pymongo
from bson.json_util import dumps
from bson.objectid import ObjectId
import json
import copy
import time
from flask import jsonify, request
import datetime
import io


# Initialize mongo connection one time
CLIENT = pymongo.MongoClient(
    f"mongodb://{env['mongodb_ip']}:{env['mongodb_port']}/")
DB = CLIENT[env['database']]


class inspections_upload(Resource):

    def post(self):
        if request.files:
            file = request.files['file']

            if '.csv' in file.filename:
                try:
                    stream = io.StringIO(
                        file.stream.read().decode("UTF8"), newline=None)
                    count = 0
                    headers = {}

                    for row_number, row in enumerate(stream):
                        values = {}
                        count += 1
                        row = row.strip()
                        row = row.split(',')

                        if row_number == 0:
                            for col_number, column in enumerate(row):
                                column = column.replace(" ", "")
                                column = column.replace(".", "")
                                headers[col_number] = column
                            continue

                        for col_number, column in enumerate(row):
                            
                            values[headers[col_number]] = column
                            
                            if headers[col_number] == "Earlstartdate":
                                date = datetime.datetime.strptime(values[headers[col_number]], '%d/%m/%Y')
                                values[headers[col_number]] = date

                            # lists
                            integers = ['Number', 'Order']
                            floats = ['Actualwork', 'Normalduration', 'Work']

                            if headers[col_number] in integers:
                                values[headers[col_number]] = int(column)
                            if headers[col_number] in floats:
                                values[headers[col_number]] = float(column)

                        DB['inspections'].find_one_and_update(
                            {
                                'Order': values['Order'],
                            },
                            {
                                '$set': values
                            },
                            upsert=True
                        )

                    # All good
                    return({'success': True, 'message': f'Processed {count} rows OK!'})
                # Error in processing (probably not a SAP export)
                except:
                    return({'success': False, 'message': f'Error processing {file.filename}'})
            # Not a .csv
            else:
                return({'success': False, 'message': f'"{file.filename}" isn\'t a .csv'})
        # No file
        else:
            return({'success': False, 'message': f'No file recieved.'})
