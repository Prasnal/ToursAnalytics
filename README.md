# ToursAnalytics

## Run project:
`source myenv/bin/activate`
`python main.py`

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
- Check migrations:
`alembic check`

## Superset
- `docker-compose -f docker-compose-non-dev.yml up`
- http://localhost:8088/


## TODO:
### Database part:
- Add scraping 24 times per day [just add datetime column with creation date that is not required], add timestamp in scraped files
- Indexes on db [2]

### Rainbow scraper:
- add starting locations and additional costs related to this
- add `wypoczynek` and `zwiedzanie+wypoczynek` tour types and scrape them 
- Add `last minute tour` information

### Refactoring:
- rootdir should be taken from env vars [1]
- Move results outside repo
- Change name of "rainbow_without_parsing" -> "rainbow"
- Change name of `test_db_adding.py` in models

### Features:

### Documentation:
- Update README file
- Add documentation about superset and visualization part

### Other:
- Add SQLs with views
- Add airflow
- Clean data
- Add database with cleaned data
- Add new dashboards
- Simple UI with email notification in case price for the tour is lower than X
- Save logs to file

## BUGS
- Not detected for now

## DONE:
- read db from env vars - https://github.com/sqlalchemy/alembic/discussions/1149 [x]
- Add CASCADE on db [x]
- nullable/unique [x]
- implement adding to db from date - to date [x]
- Check scraped tour price [x]
- add logging [x]
- Add all missing data to local db[x]
- Separate scraping and saving to db [x]
- Add command to insert data from files [x]

