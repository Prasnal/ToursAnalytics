import requests
import json
import datetime
import os
import logging

# logging.basicConfig(filename='example.log',level=logging.DEBUG) #TODO: move to settings
logging.basicConfig(level=logging.INFO)
DIR = '/home/krasnal/Projects/ToursAnalytics/'  # TODO: move to settings

# TODO: download "odpoczynek" as well
# TODO: create settings with DIR and logging
# TODO: create class RainbowToursScraper

# TODO: add exceptions and validations

# TODO: add tests
# TODO: cron to python
# TODO: create function to read data from object (and later files) to save data in db

# trip_type = 'objazd'

def get_tours_list(tour_type: str, page: int, limit: int) -> list:
    json_data = {
        'AtrybutyMulti': {
            'TypyWyjazdu': [
                tour_type
            ],
            'Lokalizacje_HoteloProdukt': [],
            'Miasta': [],
        },
        'AtrybutySingle': {
            'DlugoscPobytu': [
                '*-*',
            ],
            'Cena': [
                'avg',
            ],
            'OcenaKlientow': [
                '*-*',
            ],
            'OdlegloscLotnisko': [
                '*-*',
            ],
        },
        'DatyUrodzenia': [
            '1993-01-01',
            '1993-01-01',
        ],
        'LiczbaPokoi': 1,
        'Sortowanie': 'cena-asc',
        'CzyWeekendowka': False,
        'PowrotNaInneLotnisko': False,
        'Strona': page,
        'Limit': limit,
    }
    response = requests.post('https://r.pl/api/wyszukiwarka/wyszukaj', json=json_data)
    # TODO: check correct response
    return response.json()


def get_prices(hotel_url: str, product_url: str) -> list:
    json_data = {
        'HotelUrl': hotel_url,  # 'zakwaterowanie-prg',
        'ProduktUrl': product_url,  # 'praga-express',
        'DatyUrodzenia': [
            '1993-01-01',
            '1993-01-01',
        ],
        # 'Wyzywienie': 'sniadania',
        'CzyV2': True,
    }
    response = requests.post('https://r.pl/api/wyszukiwarka/wyszukaj-kalkulator', json=json_data)
    #TODO: check correct response
    return response.json()


def get_tour_details(tour_id: str, price: str, price_without_promo: str, params: dict) -> list:
    data = {
        'Parametry': [
            {
                'Id': tour_id,
                'Cena': price,
                'CenaBezPromocji': price_without_promo,
                'CenyZaOsoby': [
                    {},
                    {},
                ],
                'Params': params,
            },
        ],
        'CzyCenaZaOsobe': True,
        'DatyUrodzenia': [
            '1993-01-01',
            '1993-01-01',
        ],
        'LiczbaPokoi': 1,
        'Route': '/wycieczki-objazdowe',
    }

    response = requests.post('https://r.pl/api/bloczki/pobierz-bloczki', json=data)
    # TODO: check correct response
    return response.json()


def merge_tours() -> list:
    page_number = 0
    count_results = 1
    results = list()
    while count_results > 0:
        page_number += 1
        response = get_tours_list('objazd', page_number, limit=10)
        result = response['Wynik']
        count_results = len(result)
        results.extend(result)
    return results


def get_product_url(result: dict) -> str:
    google_url = result['BazoweInformacje']['OfertaURLDlaGoogle'].split('/')
    logging.info(google_url)
    #TODO: check if index exist
    return google_url[1]


def get_hotel_url(result: dict) -> str:
    google_url = result['BazoweInformacje']['OfertaURLDlaGoogle'].split('/')
    logging.info(google_url)
    #TODO: check if index exist
    return google_url[2]


def read_from_obj():
    pass


def read_from_file():
    pass


def save_json_to_file(data: list, file_name: str) -> None:
    today = datetime.date.today().strftime('%d-%m-%Y')
    json_object = json.dumps(data, indent=4)
    file_name_with_date = f'{file_name}-{today}.json'

    path = DIR + f'results/{today}/' #TODO: in path should be also name of the scraper /Rainbow/
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)

    with open(path + file_name_with_date, "w") as outfile:
        outfile.write(json_object)


def main(save_to_json: bool) -> None:
    tours = merge_tours()

    for tour in tours:
        logging.info(tour)
        tour_id = tour['Id']
        price = tour['Cena']
        price_without_promo = tour['CenaBezPromocji']
        params = tour['Params']
        tour_details = get_tour_details(tour_id, price, price_without_promo, params)[0]
        logging.info("DETAILS:")
        logging.info(tour_details)

        link = get_product_url(tour_details) #google_url[1]  # 'praga-express'# result['BazoweInformacje']['OfertaURL'].split('/')[0]
        hotel = get_hotel_url(tour_details) #google_url[2]  # 'zakwaterowanie-prg' #link.split('/')[2].split('?')[0]

        prices = get_prices(hotel, link)

        merged_results = {
            "Tour": tour,
            "TourDetails": tour_details,
            "Prices": prices
        }

        if save_to_json:
            save_json_to_file(merged_results, link)
    if save_to_json:
        save_json_to_file(tours, f'all-results')


main(save_to_json=True)
