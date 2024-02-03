import logging
from datetime import datetime
from datetime import timedelta
import json
import os
from scrapers import rainbow_without_parsing
logging.basicConfig(level=logging.INFO)

from models.test_db_adding import add_data_to_database
from utils.add_scraped_files import add_to_db_scraped_files

from models.connection import engine, Base
import traceback
import argparse

#TODO: photos should be many to many [NOT RELEVANT NOW, leave it as it is until we need photos]
#TODO: get_or_create for tours should filter only via tour_url, tour_name can be different
#TODO: add locations and additional costs
#TODO: check if it's saved in the same catalog on the server

def add_jsons_to_db(start_date, end_date):
    if not end_date:
        end_date = start_date
    add_to_db_scraped_files(start_date, end_date)


#################### DROPPING DB #############################
# Base.metadata.drop_all(engine)
# Base.metadata.create_all(engine)
##############################################################

#add_to_db_scraped_files('01-01-2024', '03-01-2024')
#rainbow_without_parsing.main_rainbow(save_to_json=True, save_to_db=True)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
            description="The program scrape tour offices websites to gather data about tour prices."
        )
    parser.add_argument("--start_date", required=False, type=str, help="Save data from files in database from start_date")
    parser.add_argument("--end_date", required=False, type=str, help="Save data from files in database till end_date")
    parser.add_argument("--clean_db", action='store_true', help="Drop DB")

    args = parser.parse_args()

    if args.clean_db:
        Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)
    elif args.start_date:
        end_date = args.end_date
        if not end_date:
            end_date = args.start_date
        add_to_db_scraped_files(args.start_date, end_date)
    else:
        today = datetime.today().strftime('%d-%m-%Y')
        #tour_obj = rainbow_without_parsing.main_rainbow(save_to_json=True)
        add_to_db_scraped_files(today, today) #TODO: modify to one argument
