import logging
import tarfile
import os
import shutil
import json
import gzip
from datetime import datetime, timedelta, date


rootdir = '../scraper/results/'

def gzip_date(tour_operator, date_to_gzip):
    # if type(date) == datetime.datetime:
    date_str = date_to_gzip.strftime('%Y-%m-%d')

    path = f'results/{tour_operator}/{date_str}'
    if os.path.exists(path):
        if not os.path.exists(path +'.tar.gz'):
            with tarfile.open(path + ".tar.gz", "w:gz") as tar:
                tar.add(path, arcname=date_str)
                logging.info("Created gzip for {}".format(date_str))
        else:
            logging.info("GZIP with results for {} already exists".format(date_str))
    else:
        logging.warning("Didn't find any results for {}".format(date_str))


def remove_directory_if_tarred(path):
    tarred_path = f'{path}.tar.gz'
    if os.path.exists(path):
        if os.path.exists(tarred_path):
            if os.path.getsize(tarred_path) > 100:
                logging.info("file size {}".format(os.path.getsize(tarred_path)))
                shutil.rmtree(path)
                logging.info("Folder {} was removed".format(path))
            else:
                logging.info("Gzip is too small so data won't be deleted (are files properly packed?)")
        else:
            logging.info(
                f"Tarred file: {tarred_path} doesn't exist so data won't be deleted as there is no backup")
    else:
        logging.info("Path: {} doesn't exist so cannot be deleted ".format(path))



def save_json_to_gz_file(tour_operator, data, tour_name: str) -> None:
    today = date.today().strftime('%Y-%m-%d')
    timestamp = datetime.now().isoformat()
    json_object = json.dumps(data, indent=4)
    file_name_with_date = f'{tour_name}_{timestamp}.json.gz'

    path = f'results/{tour_operator}/{today}/{tour_name}/'
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)

    with gzip.open(path + file_name_with_date, 'wt') as outfile:
        outfile.writelines(json_object)

    return path+file_name_with_date



def generate_dates_between(start_date: str, end_date: str) -> list[str]:
    start = datetime.strptime(start_date, '%Y-%m-%d')
    end = datetime.strptime(end_date, '%Y-%m-%d')

    datetime_list = [start+timedelta(days=x) for x in range((end-start).days)]
    date_str_list=list(map(lambda x: x.strftime('%Y-%m-%d'), datetime_list))
    date_str_list.append(end_date)

    return date_str_list


def add_to_db_latest_files(tour_office, start_date, end_date):
    catalog_names = generate_dates_between(start_date, end_date)
    for date in catalog_names:
        path = rootdir + tour_office + '/' + date
        logging.info(f"Path: {path}")
        try:
            catalogs = os.listdir(path)
        except FileNotFoundError:
            logging.warning(f"Catalog {date} doesn't exist")
            continue
        for tour_name in catalogs:
            try:
                files = os.listdir(path + '/' + tour_name)
            except FileNotFoundError:
                logging.warning(f"Catalog {date} doesn't exist")
                continue


def extract_directory(path):
    main_path = os.path.dirname(path)
    with tarfile.open(path, 'r') as tar:
        tar.extractall(main_path)

def create_path(tour_operator, date, tarred):
    raise NotImplementedError

