import requests

from models.test_db_adding import add_data_to_database
#from bs4 import BeautifulSoup
from scrapers import rainbow_without_parsing

#TODO: photos should be many to many
#TODO: get_or_create for tours should filter only via tour_url, tour_name can be different
#TODO: add start date and end_date when adding to db from files
#TODO: add proper logs and error logs

#TODO: fix save_to_json
# TODO: add country to the tour
#TODO: add locations and additional costs
#TODO: db reformatting (cascade delete, models nullable, unique etc.
#TODO: read obj and save to db from files
#TODO: check if it's saved in the same catalog on the server

#rainbow_without_parsing.main_rainbow(save_to_json=True, save_to_db=True)


from datetime import datetime
##### read from file test:
import json
#from test_db_adding import add_data_to_database
import os
rootdir = '/home/krasnal/Projects/my_projects/ToursAnalytics/scraper/results/'

for subdir, dirs, files in os.walk(rootdir):
    for file in files:
        scraped_date = subdir.split('/')[-1]
        print("date:", scraped_date)
        path_to_file = os.path.join(subdir, file)
        print("PATH TO FILE:", path_to_file)

        with open(path_to_file) as f:
            data = json.load(f)
            #print(data)
            try:
                obj = rainbow_without_parsing.RainbowParser(data).create_tour()
            except Exception:
                print("NIE UDALO SIE POBRAC WYCIECZKI:", path_to_file)
                continue
            #print("OBJ:", obj)
            add_data_to_database(obj, datetime.strptime(scraped_date, '%d-%m-%Y'))
