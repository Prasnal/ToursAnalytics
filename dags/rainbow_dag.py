import json

import sys
import os
sys.path.append(os.path.abspath('/home/krasnal/Projects/my_projects/ToursAnalytics/scraper'))
import pendulum
from airflow.decorators import dag, task
from scrapers.rainbow import main_rainbow
# from utils.add_scraped_files import add_files_to_db

@dag(
    schedule=None,
    start_date=pendulum.datetime(2024, 1, 1, tz="UTC"),
    catchup=False,
    tags=["Rainbow"],
)
def rainbow_daily_pipeline():
    @task()
    def scrape():
        tours_details = main_rainbow(save_to_json=True)
        created_files = [tour_details['path'] for tour_details in tours_details.values()]

        return created_files

    # Airflow supports SQLALchemy only below version 2.0.0,
    # SQLAlchemy related code, was implemented before using airflow
    # and uses features that are supported only on> 2.0.0
    # #TODO: add caching virtualenv
    @task.virtualenv(
        task_id="add_to_db",
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
        system_site_packages=False
    )
    def add_to_db(scraped_data: list):
        import sys
        sys.path.insert(0, '/home/krasnal/Projects/my_projects/ToursAnalytics/scraper')
        from utils.add_scraped_files import add_files_to_db
        add_files_to_db(scraped_data)

    scraped_data = scrape()
    add_to_db(scraped_data)


rainbow_daily_pipeline()


