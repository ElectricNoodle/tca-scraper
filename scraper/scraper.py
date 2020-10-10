import time
import urllib.request
import re
import threading
import ast
import datetime
from bs4 import BeautifulSoup
from influxdb import InfluxDBClient
import os

influx_db_user = os.environ['INFLUXDB_USER']
influx_db_user = os.environ['INFLUXDB_PASSWORD']

scrape_url = "https://portal.rockgympro.com/portal/public/d0f355e237dda999f3112d94d3c762c7/occupancy"
SCRAPE_INTERVAL = 300
scrape_regex = re.compile('var data = (.*?);', re.DOTALL | re.MULTILINE)

client = InfluxDBClient('influxdb', 8086, 'admin', 'admin', 'tca')

def scrape_data():
    fp = urllib.request.urlopen(scrape_url)
    mybytes = fp.read()

    html = mybytes.decode("utf8")
    fp.close()

    soup = BeautifulSoup(html, 'html.parser')
    scripts = soup.find_all('script')

    data = scrape_regex.search(str(scripts[2].string))
    print(scripts[2])

    if data:
        save_data(data.group(1))

    threading.Timer(SCRAPE_INTERVAL, scrape_data).start()


def save_data(raw_data):

    data = ast.literal_eval(raw_data)
    time = datetime.datetime.now()

    gyms = {'The Mothership':'BRI', 'The Church': 'UNC', 'The Newsroom': 'GLA', 'The Prop Store' : 'PST'};

    for gym in gyms.keys():
        gym_code = gyms[gym]
        json_body = [
                {
                    "measurement": 'occupancy',
                    "tags": {
                        "gym_code": gym_code,
                    },
                    "time": time.isoformat(),
                    "fields": {
                        "value": data[gym_code]['capacity']
                    }
                }
            ]
        client.write_points(json_body)
    
scrape_data()
