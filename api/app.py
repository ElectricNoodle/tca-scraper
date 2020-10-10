from flask import Flask, jsonify, request
from influxdb import InfluxDBClient
from datetime import datetime, timedelta

client = InfluxDBClient('influxdb', 8086, 'admin', 'admin', 'tca')

app = Flask(__name__)

@app.route('/', methods=['GET'])
@app.route('/<gym_code>', methods=['GET'])
def values(gym_code="all"):
    startTime = request.args.get('from')
    
    endTime = request.args.get('to')

    if startTime is not None:
        try:
            startTime = datetime.strptime(startTime, "%Y-%m-%dT%H:%M:%S%z").isoformat()
        except ValueError:
            startTime = (datetime.now() - timedelta(hours = 1)).isoformat()
    
    if endTime is not None:
        try:
            endTime = datetime.strptime(endTime, "%Y-%m-%dT%H:%M:%S%z").isoformat()
        except ValueError:
            startTime = datetime.now().isoformat()

    gym_codes = ['BRI', 'UNC', 'GLA', 'PST']

    whereStatement = ''
    if gym_code != 'all':
        if gym_code in gym_codes:
            whereStatement = ' AND ("gym_code"=\'' + gym_code + '\')'

    results = client.query('SELECT mean("value") AS "mean_value" FROM "tca"."autogen"."occupancy" WHERE time >= \'' + startTime + '\' AND time <= \'' + endTime + '\'' + whereStatement + ' GROUP BY time(5m), "gym_code"')
    return jsonify(results.raw)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')