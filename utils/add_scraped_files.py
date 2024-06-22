import logging
import os
import gzip
import json
import traceback
from scrapers import rainbow
logging.basicConfig(level=logging.INFO)

from models.test_db_adding import add_data_to_database
from utils.utils import generate_dates_between, extract_directory, remove_directory_if_tarred



#TODO: move rootdir as env var
rootdir = '../scraper/results/'


def add_files_to_db(files_list):
    for full_path in files_list:
        with gzip.open(full_path, 'r') as f:
            timestamp = full_path.split('_')[-1].strip('.json.gz')
            json_bytes = f.read()

        json_str = json_bytes.decode('utf-8')
        data = json.loads(json_str)

        try:
            obj = rainbow.RainbowParser(data).create_tour()
        except Exception as e:
            logging.error(f"Creating tour was not possible: {full_path}")
            traceback.print_exc()
            continue
        logging.info(f"Adding to database {full_path}:")
        add_data_to_database(obj, timestamp)


def add_to_db_all_scraped_files(tour_office, start_date, end_date, **kwargs):
    catalog_names = generate_dates_between(start_date, end_date)
    for date in catalog_names:
        path = rootdir+tour_office+'/'+date #TODO: bug, if the catalog already exists and it's not tarred - it will lbe removed!

        if not os.path.exists(path):
            tarred_path = rootdir + tour_office + '/' + date + '.tar.gz'
            if os.path.exists(tarred_path):
                extract_directory(tarred_path)

        logging.info(f"Path: {path}")
        try:
            catalogs = os.listdir(path)
        except FileNotFoundError:
            logging.warning(f"Catalog {date} doesn't exist")
            continue
        for tour_name in catalogs:
            try:
                files = os.listdir(path+'/'+tour_name)
            except FileNotFoundError:
                logging.warning(f"Catalog {date} doesn't exist")
                continue

            for file_name in files:
                full_path = f"{path}/{tour_name}/{file_name}"
                extension = full_path.split('.')[-1]

                if extension == 'gz':
                    with gzip.open(full_path, 'r') as f:
                        timestamp = file_name.split('_')[-1].strip('.json.gz')
                        json_bytes = f.read()

                    json_str = json_bytes.decode('utf-8')
                    data = json.loads(json_str)

                elif extension == 'json':
                    with open(full_path) as f:
                        timestamp = file_name.split('_')[-1].strip('.json')
                        data = json.load(f)
                else:
                    logging.warning('Not supported extension: ', extension)
                    continue

                try:
                    obj = rainbow.RainbowParser(data).create_tour()
                except Exception as e:
                    logging.error(f"Creating tour was not possible: {full_path}")
                    traceback.print_exc()
                    continue
                logging.info(f"Adding to database {file_name}:")
                add_data_to_database(obj, timestamp)

        remove_directory_if_tarred(path)





