from models.connection import Session, engine, Base
from models.countries import Country
from models.tour_agencies import TourAgency
# from models.tour_types import TourType
from models.tours import Tour
from models.photos import Photos
from models.tour_types import TourType
from models.tour_prices import TourPrice
from models.tour_configurations import TourConfig
from sqlalchemy.exc import IntegrityError
from psycopg2.errors import UniqueViolation
from datetime import datetime
import logging

# logging.basicConfig(
#     level=logging.INFO,
#     format="%(asctime)s - %(levelname)s : %(message)s",
#     datefmt="%Y-%m-%d,%H:%M:%S ",
#     handlers=[
#         logging.StreamHandler(),
#     ],
# )



def add_data_to_database(obj, timestamp):
    with Session() as session:
        logging.debug(f"Starting create objects")
        agency_obj = add_tour_agency(obj, session)
        countries_objs = add_countries(obj, session)
        tour_type_o = add_tour_type(obj, session)
        tour_obj = add_tour(obj, session, tour_type_o, agency_obj, countries_objs)
        #photo_objs = add_photos(obj, session, tour_obj)
        logging.debug(f"Finished creating objects")

        details = obj.terms_and_prices
        logging.debug(f"Started adding to db details")
        for detail in details:
            logging.debug(f"Started adding to db tour_config")
            config_obj = add_tour_config(detail, session, tour_obj)
            logging.debug(f"Finished adding to db tour_config")
            scraped_date = timestamp.split('T')[0]
            scraped_time = timestamp.split('T')[1]
            logging.debug(f"Started adding to db tour_prices")
            add_tour_price(detail, session, config_obj, scraped_date, scraped_time)
            logging.debug(f"Finished adding to db tour_prices")
        logging.debug(f"Finished adding to db details")
        # tour_prices

from sqlalchemy.dialects import postgresql
def get_or_create(session, model, defaults=None, **kwargs):
    logging.debug(f"Starting getting instance")
    query = session.query(model).filter_by(**kwargs)

    sql_query = query.statement.compile(
        dialect=postgresql.dialect(),
        compile_kwargs={"literal_binds": True}
    )
    logging.debug(f"Generated SQL for SELECT: {sql_query}")

    instance = query.one_or_none()

    logging.debug(f"Finished getting creating instance")

    if instance:
        return instance, False
    else:
        logging.debug(f"Adding instance")
        kwargs |= defaults or {}
        instance = model(**kwargs)
        try:
            session.add(instance)
            session.commit()
        except IntegrityError as e:
            if isinstance(e.orig,
                          UniqueViolation):
                session.rollback()
                instance = session.query(model).filter_by(**kwargs).one()
                return instance, False
            else:
                raise Exception("ANOTHER ERROR:", e)
        else:
            logging.debug(f"Finished adding instance")
            return instance, True



def add_tour_price(detail, session, tour_config_obj, scraped_date, scraped_time):
    tour_approved = detail.approved
    tour_price = detail.term_price
    tour_price_pp = detail.term_price_pp
    logging.debug("Start get_or_create tour_price")
    tour_price_o = get_or_create(
        session, TourPrice,
        scraped_date=scraped_date,
        scraped_time=scraped_time,
        tour_approved=tour_approved,
        tour_price=tour_price,
        tour_price_pp=tour_price_pp,
        tour_config=tour_config_obj[0],
        tour_config_id=tour_config_obj[0].id
    )
    logging.debug("Finish get_or_create tour_price")
    return tour_price_o


def add_tour_config(detail, session, tour_obj):
    tour_length = detail.length
    start_location = None
    location_additional_cost = None
    start_tour_date = detail.term_start
    end_tour_date = detail.term_end
    tour_config_o = get_or_create(
                                session,
                                TourConfig,
                                defaults={"tour_prices": []},
                                tour_length=tour_length,
                                start_location=start_location,
                                location_additional_cost=location_additional_cost,
                                start_tour_date=start_tour_date,
                                end_tour_date=end_tour_date,
                                tour=tour_obj[0],
                                tour_id=tour_obj[0].id
                                  )

    return tour_config_o


def add_tour_type(obj, session):
    tour_type = obj.tour_type
    tour_type_o = get_or_create(session, TourType, defaults={"tours": []}, tour_type=tour_type)
    return tour_type_o


def add_tour(obj, session, tour_type_obj, tour_agency_obj, countries_objs_list):
    tour_id = obj.tour_id
    omnibus_key = obj.klucz_omnibus
    tour_name = obj.tour_name
    tour_url = obj.tour_url
    logging.info(f"Adding tour to db: {tour_name}")
    tour_obj = get_or_create(session,
                             Tour,
                             defaults={
                                 'tour_photos': [],
                                 'tour_config': [],
                                 'omnibus_key': omnibus_key,
                                 'tour_url': tour_url,
                                 'countries': countries_objs_list,
                                 'original_tour_id': tour_id,
                             },
                             #original_tour_id=tour_id,
                             tour_name=tour_name,
                             #tour_url=tour_url,
                             tour_type=tour_type_obj[0],
                             tour_type_id=tour_type_obj[0].id,
                             tour_agency=tour_agency_obj[0],
                             tour_agency_id=tour_agency_obj[0].id,

                             )
    return tour_obj


def add_photos(obj, session, tour_obj):
    photo_objs = []
    for photo_url in obj.photos:
        try:
            photo_objs.append(get_or_create(session, Photos, defaults={"tour":tour_obj[0]}, tour_id=tour_obj[0].id, photo_url=photo_url))
        except Exception:
            logging.error(f"ERROR ADDING PHOTO TO DATABASE: {photo_url}")
            continue
    return photo_objs


def add_countries(obj, session):
    countries = obj.countries
    countries_objs = list()
    for country in countries:
        countries_objs.append(get_or_create(
            session,
            Country,
            defaults={
                'tours': []
            },
            country_name=country,
            country_code=country
        )[0])
    return countries_objs


def add_tour_agency(obj, session):
    agency_name = obj.tour_agency
    url = obj.tour_agency_url
    tour_agency_obj = get_or_create(
        session,
        TourAgency,
        defaults={
            "tours": []
        },
        agency_name=agency_name,
        agency_url=url
    )
    return tour_agency_obj
