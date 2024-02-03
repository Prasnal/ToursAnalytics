import logging
from datetime import datetime
from datetime import timedelta
import json
import os
from scrapers import rainbow_without_parsing
logging.basicConfig(level=logging.INFO)

from models.test_db_adding import add_data_to_database
import traceback

#TODO: move rootdir as env var
rootdir = '/home/krasnal/Projects/my_projects/ToursAnalytics/scraper/results/'


def generate_dates_between(start_date: str, end_date: str) -> list[str]:
    start = datetime.strptime(start_date, '%d-%m-%Y')
    end = datetime.strptime(end_date, '%d-%m-%Y')
    datetime_list = [start+timedelta(days=x) for x in range((end-start).days)]
    date_str_list=list(map(lambda x: x.strftime('%d-%m-%Y'), datetime_list))
    date_str_list.append(end_date)

    return date_str_list


def add_to_db_scraped_files(start_date, end_date):
    catalog_names = generate_dates_between(start_date, end_date)
    for date in catalog_names:
        path = rootdir+date
        logging.info(f"Path: {path}")
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
                    logging.error(f"Creating tour was not possible: {full_path}")
                    traceback.print_exc()
                    continue
                logging.info(f"Adding to database {file_name}:")
                add_data_to_database(obj, datetime.strptime(date, '%d-%m-%Y'))
