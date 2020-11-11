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
influx_db_pass = os.environ['INFLUXDB_PASSWORD']

try:
    scrape_url = os.environ['SCRAPE_URL'] or "https://portal.rockgympro.com/portal/public/d0f355e237dda999f3112d94d3c762c7/occupancy"
    SCRAPE_INTERVAL = int(os.environ['SCRAPE_INTERVAL']) or 300
except KeyError:
    pass

scrape_regex = re.compile('var data = (.*?);', re.DOTALL | re.MULTILINE)

client = InfluxDBClient(
    'influxdb', 8086, influx_db_user, influx_db_pass, 'tca')


def scrape_data():
    try:
        fp = urllib.request.urlopen(scrape_url)
        mybytes = fp.read()

        html = mybytes.decode("utf8")
        fp.close()

        soup = BeautifulSoup(html, 'html.parser')
        scripts = soup.find_all('script')

        data = scrape_regex.search(str(scripts[2].string))

        if data:
            save_data(data.group(1))

        threading.Timer(15, scrape_data).start()
    except Exception:
        pass


def save_data(raw_data):
    data = ast.literal_eval(raw_data)

    gyms = {'The Mothership': 'BRI', 'The Church': 'UNC',
            'The Newsroom': 'GLA', 'The Prop Store': 'PST'}

    for gym in gyms.keys():
        gym_code = gyms[gym]

        time = data[gym_code]['lastUpdate']
        time = re.findall(r'\((.*?)\)', time)[0]
        time = datetime.datetime.strptime(time, '%I:%M %p')
        correctDateTime = datetime.datetime.combine(
            datetime.date.today(), time.time())

        try:
            count = int(data[gym_code]['count'])
            capactiy = int(data[gym_code]['capacity'])

            json_body = [
                {
                    "measurement": 'occupancy',
                    "tags": {
                        "gym_code": gym_code,
                    },
                    "time": correctDateTime.isoformat(),
                    "fields": {
                        "value": count
                    }
                }
            ]
            client.write_points(json_body)

            json_body = [
                {
                    "measurement": 'capacity',
                    "tags": {
                        "gym_code": gym_code,
                    },
                    "time": correctDateTime.isoformat(),
                    "fields": {
                        "value": capactiy
                    }
                }
            ]
            client.write_points(json_body)
        except Exception as e:
            print(data[gym_code])
            print(e.__class__)


scrape_data()
