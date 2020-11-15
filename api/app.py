from flask import Flask, jsonify, request
from flask_cors import CORS
from influxdb import InfluxDBClient
from datetime import datetime, timedelta
import os

influx_db_user = os.environ['INFLUXDB_USER']
influx_db_pass = os.environ['INFLUXDB_PASSWORD']

client = InfluxDBClient(
    'influxdb', 8086, influx_db_user, influx_db_pass, 'tca')

app = Flask(__name__)
CORS(app)


@app.route('/', methods=['GET'])
@app.route('/<gym_code>', methods=['GET'])
def values(gym_code="all"):
    startTime = request.args.get('from')
    endTime = request.args.get('to')

    if startTime is not None:
        try:
            startTime = datetime.strptime(
                startTime, "%Y-%m-%dT%H:%M:%S%z").isoformat()
        except ValueError:
            startTime = (datetime.now() - timedelta(hours=1)).isoformat()

    if endTime is not None:
        try:
            endTime = datetime.strptime(
                endTime, "%Y-%m-%dT%H:%M:%S%z").isoformat()
        except ValueError:
            endTime = datetime.now().isoformat()

    gym_codes = ['BRI', 'UNC', 'GLA', 'PST']

    if gym_code not in gym_codes:
        return ''

    try:
        capacity = client.query('SELECT DISTINCT("value") AS "capacity" FROM "tca"."autogen"."capacity" WHERE time >= \'' +
                                startTime + '\' AND time <= \'' + endTime + '\' AND ("gym_code"=\'' + gym_code + '\')  GROUP BY time(24h)')
        capacity = capacity.raw['series'][0]['values'][0][1]
    except:
        capacity = 0

    try:
        occupancy = client.query('SELECT DISTINCT("value") AS "occupancy" FROM "tca"."autogen"."occupancy" WHERE time >= \'' +
                                 startTime + '\' AND time <= \'' + endTime + '\' AND ("gym_code"=\'' + gym_code + '\')  GROUP BY time(15m)')
        occupancy = occupancy.raw['series'][0]['values']
    except:
        occupancy = []

    returnValue = {
        'gym_code': gym_code,
        'capacity': capacity,
        'occupancy': occupancy
    }

    return jsonify(returnValue)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
