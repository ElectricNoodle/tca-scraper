import time, threading, pystore,urllib.request,re
from bs4 import BeautifulSoup

data_path = "~/pystore"
data_store_name = "datastore"
collection_name = "capacity_data"

data_store = None
collection = None


scrape_url = "https://portal.rockgympro.com/portal/public/d0f355e237dda999f3112d94d3c762c7/occupancy"
SCRAPE_INTERVAL = 5
scrape_regex = re.compile('var data = (.*?);', re.DOTALL | re.MULTILINE )

def init_pystore():

    pystore.set_path(data_path)

    # Connect to datastore (create it if not exist)
    data_store = pystore.store(data_store_name)

    # Access a collection (create it if not exist)
    collection = data_store.collection(collection_name)

def scrape_data():


    fp = urllib.request.urlopen(scrape_url)
    mybytes = fp.read()

    html = mybytes.decode("utf8")
    fp.close()

    soup = BeautifulSoup(html, 'html.parser')
    scripts = soup.find_all('script')
   
    data = scrape_regex.find_all(str(scripts[2].string))
    print(scripts[2])

    if data:
        print(data)


    threading.Timer(SCRAPE_INTERVAL, main).start()

def main():
    
    init_pystore()
    scrape_data()
    
main()