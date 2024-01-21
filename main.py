import logging
from datetime import datetime
from datetime import timedelta
import json
import os
from scrapers import rainbow_without_parsing
logging.basicConfig(level=logging.INFO)

from models.test_db_adding import add_data_to_database
from models.connection import engine, Base
import traceback

#TODO: photos should be many to many [NOT RELEVANT NOW, leave it as it is until we need photos]
#TODO: get_or_create for tours should filter only via tour_url, tour_name can be different
#TODO: add locations and additional costs
#TODO: check if it's saved in the same catalog on the server


rootdir = '/home/krasnal/Projects/my_projects/ToursAnalytics/scraper/results/'

#################### DROPPING DB #############################
# Base.metadata.drop_all(engine)
# Base.metadata.create_all(engine)
##############################################################


def generate_dates_between(start_date: str, end_date: str) -> list[str]:
    start = datetime.strptime(start_date, '%d-%m-%Y')
    end = datetime.strptime(end_date, '%d-%m-%Y')
    datetime_list = [start+timedelta(days=x) for x in range((end-start).days)]
    date_str_list=list(map(lambda x: x.strftime('%d-%m-%Y'), datetime_list))
    return date_str_list
def add_to_db_scraped_files(start_date, end_date):

    catalog_names = generate_dates_between(start_date, end_date)
    for date in catalog_names:
        path = rootdir+date
        logging.info(f"PATH: {path}")
        try:
            files = os.listdir(path)
        except FileNotFoundError:
            logging.warning(f"Catalog {date} doesn't exist")
            continue
        for file_name in files:
            full_path = f"{path}/{file_name}"
            with open(full_path) as f:
                data = json.load(f)
                # print(data)
                try:
                    obj = rainbow_without_parsing.RainbowParser(data).create_tour()
                except Exception as e:
                    logging.error(f"NIE UDALO SIE STWORZYC WYCIECZKI: {full_path}")
                    traceback.print_exc()
                    continue
                logging.info(f"Adding to database {file_name}:")
                add_data_to_database(obj, datetime.strptime(date, '%d-%m-%Y'))


add_to_db_scraped_files('01-01-2024', '25-01-2024')
#rainbow_without_parsing.main_rainbow(save_to_json=True, save_to_db=True)
