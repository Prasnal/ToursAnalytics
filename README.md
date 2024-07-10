# ToursAnalytics
Purpose of this project is to analize data from travel office websites, and answer the question when is the best time to book holiday :)


To achieve the goal, I create an ETL pipline using airflow as a main tool.
For now, the project supports only one website: https://r.pl/.
Tour-related data from the website is scraped and saved in files as source of raw data. 
As the next step, data is inserted to the postgres db and it's used to create dashboards on superset.

The project is currently running on k8s (without airflow and superset for now, these tools were added recently and are only used on my local machine as WIP).
I have to tar all scraped files, as amount of inodes is limited. 
On the local machine, files are saved and read in airflow tasks, but on airflow - files can't be save&read between k8s pods,
so as the next step in the project I'm going to add MINIO.

It's still WIP project, there are a lot of things to be refactored, and as things are changing dynamically, some README
commands/info can be not up-to-date. 
Most of them are just my side-notes to remember what happens when I have some time to work on the project again.

So far, airflow pipeline is created only to add historical files to db.
You choose date of first file, and date of last file you would like to add to the db, and tour operator name:
![Selection_347.png](..%2F..%2F..%2F..%2FPictures%2FSelection_347.png)

Dates beetween are automatically generated, and insert_data tasks are created dynamically per each day:
![Selection_348.png](..%2F..%2F..%2F..%2FPictures%2FSelection_348.png)

As the next step, new DAG with adding day-to-day data will be created (retrieve_data -> clean_data -> add_to_db -> analize)
to remove current cronjob solution, and use airflow pipeline instead.

And for now, only one basic dashboard is created:
![Selection_346.png](..%2F..%2F..%2F..%2FPictures%2FSelection_346.png)

Data is scraped from January 2024 without issues.

###### Below are just mine side notes:

## Run the project:
`python3 -m venv venv`
`source myenv/bin/activate`
`pip install -r requirements.txt`
`python main.py` / `airflow standalone`

## Open db:
`psql -d testdb -U tours_user`
or
`psql -d emptydb -U tours_user`

## Commands:
`main.py -h` - help
`main.py` - Scrape data and save to file&db
`main.py --start_date 01-12-2023 --end_date 05-12-2023` - insert data from files scraped between 01 and 05 Dec (inc. 01 and 05)
`main.py --start_date 01-12-2023` - insert data from file that was created 01-12-2023
`main.py --clean_db` - remove data from db

## Migrations
- Create migration:
`alembic revision --autogenerate -m "<what happened>"`
- Run migrations:
`alembic upgrade <revision>`
  (or `alembic upgrade head`)
- Check migrations:
`alembic check`

## Running Airflow
- 

## Superset
- `docker-compose -f docker-compose-non-dev.yml up`
- http://localhost:8088/

## Tests
- `python -m unittest unittests.test_utils.TestUtilsFunctions`

## TODO:
### Database part:
- Indexes on db [2]

### Rainbow scraper:
- add starting locations and additional costs related to this
- add `wypoczynek` and `zwiedzanie+wypoczynek` tour types and scrape them 
- Add `last minute tour` information

### Refactoring:
- rootdir should be taken from env vars [1]
- Move results outside repo
- Change name of `test_db_adding.py` in models

### Features:

### Documentation:
- Add documentation about superset and visualization part

### Other:
- Add SQLs with views
- Clean data
- Add database with cleaned data
- Add new dashboards on superset
- Simple UI with email notification in case price for the tour is lower than X
- Save logs to file

