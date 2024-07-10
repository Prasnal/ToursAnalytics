import json

import sys
import os
sys.path.append(os.path.abspath('/home/krasnal/Projects/my_projects/ToursAnalytics/scraper'))
import pendulum
from airflow.decorators import dag, task, task_group
from scrapers.rainbow import main_rainbow
#from utils.add_scraped_files import add_files_to_db, test_task
from airflow.models.param import Param
import pandas as pd
from utils.utils import generate_dates_between



@dag(
    schedule=None,
    start_date=pendulum.datetime(2024, 1, 1, tz="UTC"),
    catchup=False,
    tags=["Rainbow"],
    params={
        "start_date": Param(type="string", format="date"),
        "end_date": Param(type="string", format="date"),
        "tour_offices": Param(["rainbow", "itaka"],type="array", examples=["Rainbow", "Itaka"]),
        "test_param": 3
    }
)
def add_historical():
    @task
    def generate_all_dates(**context):
        start_date = context['params']['start_date']
        end_date = context['params']['end_date']

        # all_dates_between = pd.date_range(start_date, end_date)
        all_dates_between = generate_dates_between(start_date, end_date)
        print("Date range:", all_dates_between)
        return all_dates_between



    @task_group(
        group_id="insert_historic_data_to_db"
    )
    def insert_historic_data_to_db(days):
        #  # Airflow supports SQLALchemy only below version 2.0.0,
        # # SQLAlchemy related code, was implemented before using airflow
        # # and uses features that are supported only on> 2.0.0
        # # #TODO: add caching virtualenv
        @task.virtualenv(
            # task_id="insert_data",
            requirements=[
                "alembic==1.13.1",
                "certifi==2023.11.17",
                "charset-normalizer==3.3.2",
                "greenlet==3.0.3",
                "idna==3.6",
                "Mako==1.3.2",
                "MarkupSafe==2.1.5",
                "numpy==1.26.3",
                "pandas==2.2.0",
                "psycopg2==2.9.9",
                "python-dateutil==2.8.2",
                "python-dotenv==1.0.1",
                "pytz==2023.3.post1",
                "requests==2.31.0",
                "six==1.16.0",
                "SQLAlchemy==2.0.25",
                "SQLAlchemy-Utils==0.41.1",
                "typing_extensions==4.9.0",
                "tzdata==2023.4",
                "urllib3==2.1.0",
            ],
            venv_cache_path="/tmp/",
        )
        def insert_data(day):
            import sys
            sys.path.insert(0, '/home/krasnal/Projects/my_projects/ToursAnalytics/scraper')
            from utils.add_scraped_files import add_to_db_all_scraped_files,insert_one_day_to_db
            #add_to_db_all_scraped_files(tour_office="Rainbow", start_date=day, end_date=day)
            insert_one_day_to_db('Rainbow', day)
            print(day)
            return day

        insert_data(days)



    # result = add_to_db('{{ params.tour_offices }}', '{{ params.start_date }}', '{{ params.end_date }}')
    date_list = generate_all_dates()
    insert_historic_data_to_db.expand(days=date_list)



add_historical()


