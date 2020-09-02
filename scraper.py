import time, threading, tstables,tables,urllib.request,re,ast,datetime
import pandas as pd
from bs4 import BeautifulSoup


class TCAData(tables.IsDescription):
    code = tables.StringCol(64)
    name = tables.StringCol(64)
    capacity = tables.IntCol(pos=2)
    count = tables.IntCol(pos=3)
    timestamp = tables.Float64Col(pos=4)






scrape_url = "https://portal.rockgympro.com/portal/public/d0f355e237dda999f3112d94d3c762c7/occupancy"
SCRAPE_INTERVAL = 5
scrape_regex = re.compile('var data = (.*?);', re.DOTALL | re.MULTILINE )

f = tables.open_file('tca.h5','a')

# Create a new time series
ts = f.create_ts('/','BPI',TCAData)

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
  
    data= ast.literal_eval(raw_data)
    time = datetime.datetime.now()

    data = {'GymCode':  ['BRI', 'UNC', 'GLA', 'PST'],
        'GymName': ['The Mothership', 'The Church', 'The Newsroom', 'The Prop Store'],
        'Capacity': [data['BRI']['capacity'], data['UNC']['capacity'], data['GLA']['capacity'], data['PST']['capacity']],
        'Count': [data['BRI']['count'], data['UNC']['count'], data['GLA']['count'], data['PST']['count']],
        'Time':[time,time,time,time]
    }

    print(data)
    
    df = pd.DataFrame (data, columns = ['GymCode', 'GymName', 'Capacity', 'Count','Time'])
    ts.append(df)
    print (df)

scrape_data()