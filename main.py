import logging
import argparse

from datetime import datetime
from datetime import timedelta
from utils.utils import gzip_date, remove_directory_if_tarred
from scrapers import rainbow
from utils.add_scraped_files import add_to_db_all_scraped_files, add_files_to_db
from models.connection import engine, Base

logging.basicConfig(level=logging.INFO)


#TODO: photos should be many to many [NOT RELEVANT NOW, leave it as it is until we need photos]
#TODO: get_or_create for tours should filter only via tour_url, tour_name can be different
#TODO: add locations and additional costs
#TODO: check if it's saved in the same catalog on the server

#################### DROPPING DB #############################
# Base.metadata.drop_all(engine)
# Base.metadata.create_all(engine)
##############################################################

#add_to_db_scraped_files('01-01-2024', '03-01-2024')
#rainbow.main_rainbow(save_to_json=True, save_to_db=True)

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

        add_to_db_all_scraped_files('Rainbow', args.start_date, end_date)
    else:
        today = datetime.today()
        yesterday = today - timedelta(days=1)
        try:
            gzip_date('Rainbow', yesterday)
        except Exception as e:
            logging.error("Error parsing results to gzip {}".format(e))
        else:
            path = f'results/Rainbow/{yesterday.strftime('%Y-%m-%d')}'
            remove_directory_if_tarred(path)

        tours_details = rainbow.main_rainbow(save_to_json=True)
        created_files = [tour_details['path'] for tour_details in tours_details.values()]
        add_files_to_db(created_files)
