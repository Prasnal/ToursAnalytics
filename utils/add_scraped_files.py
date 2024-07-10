import logging
import os
import gzip
import json
import traceback
from scrapers import rainbow
logging.basicConfig(level=logging.INFO)

from models.test_db_adding import add_data_to_database
from utils.utils import generate_dates_between, extract_directory, remove_directory_if_tarred

# TODO: refactor this part!!!!


#TODO: move rootdir as env var
# rootdir = '../scraper/results/'
rootdir = '/home/krasnal/Projects/my_projects/ToursAnalytics/scraper/results/'


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


# TODO: this should be implemented to be possible raise an exception if file is missing for airflow
# TODO: but continue in external script runs
def create_path_to_folder(tour_operator, date, extension=None):
    path = rootdir + tour_operator + '/' + date
    if extension:
        return path + '.' + extension
    else:
        return path

def create_path_to_tour_folder(tour_operator, date, tour, extension=None):
    path = rootdir + tour_operator + '/' + date + '/' + tour
    if extension:
        return path + '.' + extension
    else:
        return path


def create_path_to_file(tour_operator, date, tour_name, file_name, file_extension=None):
    path_to_catalog = create_path_to_folder(tour_operator, date)
    if file_extension:
        path_to_file = path_to_catalog + '/' + tour_name + '/' + file_name + '.' + file_extension
    else:
        path_to_file = path_to_catalog + '/' + tour_name + '/' + file_name

    return path_to_file

def get_timestamp_from_file(file_name):
    timestamp = file_name.split('_')[-1].replace('.json', '').replace('.gz', '')
    return timestamp

# TODO: fix
def read_file_to_json(full_path, extension): #TODO: remove extension and file_name
    if extension == 'gz' or extension == 'json.gz':
        with gzip.open(full_path, 'r') as f:
            json_bytes = f.read()
        json_str = json_bytes.decode('utf-8')
        try:
            data = json.loads(json_str)
        except Exception as e:
            logging.error(f"Exception loading json file for {full_path}: {e}")

    elif extension == 'json':
        with open(full_path) as f:
            data = json.load(f)
    else:
        logging.warning('Not supported extension: ', extension)

    return data


def insert_json_to_db(json_data, timestamp, path):
    try:
        obj = rainbow.RainbowParser(json_data).create_tour()
    except Exception as e:
        logging.error(f"Creating tour was not possible: {path}")
        raise e
    logging.info(f"Adding to database {path}:")
    add_data_to_database(obj, timestamp)

def detect_compression(path, name=None):
    if len(path.split('.')) > 2:
        return '.'.join(path.split('.')[2:])

    elif len(path.split('.')) > 1:
        return '.'.join(path.split('.')[1:])

    if name:
        path = path + name
    if os.path.exists(path):
        return ''
    elif os.path.exists(path + '.tar.gz'):
        return 'tar.gz'
    elif os.path.exists(path + '.tgz'):
        return 'tgz'
    elif os.path.exists(path + '.json.gz'):
        return 'json.gz'
    else:
        print("ERROR - catalog or file doesn't exist or extension not known")

def insert_one_day_to_db(tour_operator, date):
    date_path = create_path_to_folder(tour_operator, date)
    extension = detect_compression(date_path)
    full_path = date_path

    if extension:
        full_path = date_path + '.' + extension
        extract_directory(full_path)
    logging.info(f"Path: {full_path}")

    try:
        catalogs = os.listdir(full_path)
    except FileNotFoundError:
        logging.warning(f"Catalog {full_path} doesn't exist") #TODO: it's not possible, remove
    except Exception as e:
        logging.error("Unknown error {}".format(e))

    for tour_name in catalogs:
        insert_one_tour_to_db(tour_operator, date, tour_name)


def insert_one_tour_to_db(tour_operator, date, tour_name):
    path_to_tours = create_path_to_tour_folder(tour_operator, date, tour_name)
    try:
        tour_files = os.listdir(path_to_tours)
    except FileNotFoundError:
        logging.warning(f"Catalog {date} doesn't exist")
    except Exception:
        logging.error("Unknown error")  # TODO: better handling

    for tour_file_with_extension in tour_files:
        insert_single_file_to_db(tour_operator, date, tour_name, tour_file_with_extension)

def insert_single_file_to_db(tour_operator, date, tour_name, tour_file_with_extension, extension=None):
    print("TOUR FILE WITH EXTENSION:", tour_file_with_extension)
    extension = detect_compression(tour_file_with_extension)

    path_to_file = create_path_to_file(tour_operator, date, tour_name, tour_file_with_extension)
    tour_json = read_file_to_json(path_to_file, extension)
    timestamp = get_timestamp_from_file(tour_file_with_extension) #TODO: fix

    try:
        obj = rainbow.RainbowParser(tour_json).create_tour()
    except Exception as e:
        logging.error(f"Creating tour was not possible: {path_to_file}")
        traceback.print_exc()
    logging.info(f"Adding to database {tour_file_with_extension}:")
    add_data_to_database(obj, timestamp)

#TODO: this is old part of code, refactoring is WIP - this function should use functions implemented above
def add_to_db_all_scraped_files(tour_office, start_date, end_date, **kwargs):
    catalog_names = generate_dates_between(start_date, end_date)
    for date in catalog_names:
        path = rootdir+tour_office+'/'+date #TODO: bug, if the catalog already exists and it's not tarred - it will lbe removed!

        if not os.path.exists(path):
            tarred_path = rootdir + tour_office + '/' + date + '.tar.gz'
            if os.path.exists(tarred_path):
                extract_directory(tarred_path)
            else:
                print("TARRED PATH DOESNT EXIST!")

        logging.info(f"Path: {path}")
        try:
            catalogs = os.listdir(path)
        except FileNotFoundError:
            logging.warning(f"Catalog {date} doesn't exist")
            continue
        except Exception:
            logging.error("Unknown error")  # TODO: better handling
            continue
        for tour_name in catalogs:
            try:
                files = os.listdir(path+'/'+tour_name)
            except FileNotFoundError:
                logging.warning(f"Catalog {date} doesn't exist")
                continue
            except Exception:
                logging.error("Unknown error") #TODO: better handling
                continue

            for file_name in files:
                full_path = f"{path}/{tour_name}/{file_name}"
                extension = full_path.split('.')[-1]

                if extension == 'gz':
                    with gzip.open(full_path, 'r') as f:
                        timestamp = file_name.split('_')[-1].strip('.json.gz')
                        json_bytes = f.read()

                    json_str = json_bytes.decode('utf-8')
                    try:
                        data = json.loads(json_str)
                    except Exception as e:
                        logging.error(f"Exception loading json file for {file_name}: {e}")
                        continue

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





