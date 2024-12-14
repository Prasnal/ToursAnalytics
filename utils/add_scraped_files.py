import logging
from datetime import datetime
from datetime import timedelta
import json
import os
from scrapers import rainbow_without_parsing
from scrapers.rainbow_without_parsing import delete_folder
import tarfile
from models.test_db_adding import add_data_to_database
import traceback
import gzip

#TODO: move rootdir as env var
rootdir = '../scraper/results/'


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


def rename_tar_gz_to_tgz(directory):
    try:
        for catalog_name in os.listdir(directory):
            for filename in os.listdir(directory+'/'+catalog_name):
                if filename.endswith(".tar.gz"):
                    old_file = os.path.join(directory+'/'+catalog_name, filename)
                    new_file = os.path.join(directory+'/'+catalog_name, filename.replace(".tar.gz", ".tgz"))
                    os.rename(old_file, new_file)
                    print(f"Renamed: {old_file} -> {new_file}")
    except Exception as e:
        print(f"An error occurred: {e}")


#todo: add possibility to add to db only last file from tour (for main parser)
def add_to_db_scraped_files(tour_office, start_date, end_date, only_last_file=False, **kwargs):
    catalog_names = generate_dates_between(start_date, end_date)
    for date in catalog_names:
        untarred_path = rootdir+tour_office+'/'+date
        tarred_path = f"{rootdir}{tour_office}/{date}.tgz"

        if os.path.isdir(untarred_path):
            is_tarred = False
        elif os.path.isfile(tarred_path):
            is_tarred = True
        else:
            logging.warning(f"Catalog {date} doesn't exist")
            continue

        if is_tarred:
            temp_dir = f"{untarred_path}"
            try:
                os.makedirs(temp_dir, exist_ok=False)
                with tarfile.open(tarred_path, "r:gz") as tar:
                    tar.extractall(temp_dir)
                path = temp_dir + f'/{date}'
                print("PATH:", path)
            except Exception as e:
                logging.error(f"Failed to extract tar file {tarred_path}: {e}")
                traceback.print_exc()
                continue

        else:
            path = untarred_path

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
            if kwargs.get('specific_file_name'):
                file_name = kwargs['specific_file_name']
            else:
                files.sort()
                # last_file_name = files[0]
            if only_last_file:
                # print("FILES SORETED:", files)
                files = [files[-1]] # - sprawdzic sortowanie

            for file_name in files:
                full_path = f"{path}/{tour_name}/{file_name}"
                extension = full_path.split('.')[-1]

                if extension == 'gz':
                    with gzip.open(full_path, 'r') as f:
                        timestamp = file_name.split('_')[-1].strip('.json.gz')
                        json_bytes = f.read()

                    try:
                        json_str = json_bytes.decode('utf-8')
                        data = json.loads(json_str)
                    except Exception as e:
                        logging.error(f"Failed to read json file: {file_name}")
                        continue

                elif extension == 'json':
                    with open(full_path) as f:
                        timestamp = file_name.split('_')[-1].strip('.json')
                        data = json.load(f)
                else:
                    logging.warning(f'Not supported extension: {extension}' )
                    continue

                try:
                    obj = rainbow_without_parsing.RainbowParser(data).create_tour()
                except Exception as e:
                    logging.error(f"Creating tour was not possible: {full_path}")
                    traceback.print_exc()
                    continue
                logging.info(f"Adding to database {file_name}:")
                add_data_to_database(obj, timestamp)

        if is_tarred:
            date_dt = datetime.strptime(date, '%Y-%m-%d')
            delete_folder(tour_office, date_dt)





