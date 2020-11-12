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

    whereStatement = ''
    if gym_code != 'all':
        if gym_code in gym_codes:
            whereStatement = ' AND ("gym_code"=\'' + gym_code + '\')'

    results = client.query('SELECT distinct("value") AS "mean_value" FROM "tca"."autogen"."occupancy" WHERE time >= \'' +
                           startTime + '\' AND time <= \'' + endTime + '\'' + whereStatement + ' GROUP BY time(15m), "gym_code"')
    return jsonify(results.raw)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
