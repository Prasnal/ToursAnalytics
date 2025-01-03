import requests
import json
import datetime
import os
import sys
sys.path.insert(0,'/home/krasnal/Projects/my_projects/ToursAnalytics/scraper') #TODO: change this
from tours.tour import Tour, TermsDetails
import logging
import gzip, tarfile, shutil

DIR = '/home/krasnal/Projects/my_projects/ToursAnalytics/scraper'  # TODO: move to settings

# TODO: download "odpoczynek" as well
# TODO: create settings with DIR and logging
# TODO: create class RainbowToursScraper
# TODO: add exceptions and validations
# TODO: add tests
# TODO: add files extension as param for scraping

# trip_type = 'objazd'
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s.%(msecs)03d - %(levelname)s : %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.StreamHandler(),
        # logging.FileHandler("test.log", "a"),
    ],
)

def gzip_date(tour_operator, date):
    # if type(date) == datetime.datetime:
    date = date.strftime('%Y-%m-%d')

    path = f'results/{tour_operator}/{date}'
    if os.path.exists(path):
        if not os.path.exists(path +'.tgz'):
            with tarfile.open(path + ".tgz", "w:gz") as tar:
                tar.add(path, arcname=date)
        else:
            logging.info("GZIP with results for {} already exists".format(date))
    else:
        logging.warning("Didn't find any results for {}".format(date))


def delete_folder(tour_operator, date):
    # if type(date) == datetime.datetime:
    date = date.strftime('%Y-%m-%d')
    path = f'results/{tour_operator}/{date}'
    path_gzip = f'results/{tour_operator}/{date}'+'.tgz'
    path_targz = f'results/{tour_operator}/{date}'+'.tar.gz'

    if os.path.isfile(path_gzip):
        tarred_path = path_gzip
    elif os.path.isfile(path_targz):
        tarred_path = path_targz
    else:
        logging.warning("GZIP with results for {} doesn't exist".format(date))

    if os.path.exists(path) and os.path.getsize(tarred_path) > 100:
        logging.info("file size {}".format(os.path.getsize(tarred_path)))
        shutil.rmtree(path)
        logging.info("Folder {} was removed".format(path))
    else:
        logging.info("Path: {} doesn't exist so cannot be deleted or gzip is too small (are files properly packed?)".format(path))



def save_json_to_gz_file(tour_operator, data, tour_name: str) -> None:
    today = datetime.date.today().strftime('%Y-%m-%d')
    timestamp = datetime.datetime.now().isoformat()
    json_object = json.dumps(data, indent=4)
    file_name_with_date = f'{tour_name}_{timestamp}.json.gz'

    path = f'results/{tour_operator}/{today}/{tour_name}/'
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)

    with gzip.open(path + file_name_with_date, 'wt') as outfile:
        outfile.writelines(json_object)

def save_json_to_file(tour_operator, data, tour_name: str) -> None:
    today = datetime.date.today().strftime('%Y-%m-%d')
    timestamp = datetime.datetime.now().isoformat()
    json_object = json.dumps(data, indent=4)
    file_name_with_date = f'{tour_name}_{timestamp}.json'

    path = f'results/{tour_operator}/{today}/{tour_name}/'
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)

    with open(path + file_name_with_date, "w") as outfile:
        outfile.write(json_object)


class RainbowParser:
    def __init__(self, tour_json):
        #print("JSON", tour_json)
        self.tour_json = tour_json
        self.tour_agency = 'Rainbow'
        self.tour_agency_url = "https://r.pl/"
        self.tour_name = tour_json["TourDetails"]["BazoweInformacje"]["OfertaNazwa"]
        self.countries = tour_json["TourDetails"]["BazoweInformacje"]["Panstwa"]
        self.tour_type = tour_json["TourDetails"]["BazoweInformacje"]["TypWycieczki"]
        # self.tour_url= tour_json["TourDetails"]["BazoweInformacje"]["OfertaURL"]
        self.tour_url= tour_json["TourDetails"]["BazoweInformacje"]["OfertaURLDlaGoogle"]


        self.grade=tour_json["TourDetails"]["Ocena"]['Ocena']
        self.photos=tour_json["TourDetails"]["Zdjecia"]

        self.full_tour_id = tour_json['Tour']['Id']
        self.tour_id = tour_json['Tour']['Id'].split(':')[0]
        try:
            self.klucz_omnibus= tour_json['Tour']['KluczOmnibusaKwalifikowany']
        except Exception:
            self.klucz_omnibus = None

        self.start_locations = []
        # food_plans = tour_json["TourDetails"]["Wyzywienia"]
        # TODO: last minute?

    def get_terms_and_prices(self):
        if not self.tour_json["Prices"]["Terminy"]:
            return list()

        terms_length = self.tour_json["Prices"]["Terminy"]
        terms_details_list = list()
        for term_by_length in terms_length:
            term_length = term_by_length["Dlugosc"]
            terms = term_by_length["Terminy"]
            for term in terms:
                start_date = term["Termin"]
                end_date = term["DataKoniec"]
                nights = term["LiczbaNocy"]
                price = term["Cena"]
                per_person_price = term["CenaZaOsobe"]
                active = term["CzyAktywna"]
                approved = term["CzyPotwierdzony"]

                terms_details_obj = TermsDetails(start_date, end_date, price, per_person_price, nights, approved, term_length) #TODO: exceptions
                terms_details_list.append(terms_details_obj) #TODO: exceptions

        return terms_details_list

    def create_tour(self):
        tour_obj = Tour(
            tour_agency=self.tour_agency,
            tour_agency_url=self.tour_agency_url,
            tour_name=self.tour_name,
            countries=self.countries,
            tour_type=self.tour_type,
            tour_url=self.tour_url,
            klucz_omnibus=self.klucz_omnibus,
            tour_id=self.tour_id,
            terms_and_prices=self.get_terms_and_prices(),
            start_locations=self.start_locations,
            grade=self.grade,
            photos=self.photos
        )
        return tour_obj


class RainbowScraper:
    def get_prices(self, tour_details) -> list:
        json_data = {
            'HotelUrl': self.get_hotel_url(tour_details),  # 'zakwaterowanie-prg',
            'ProduktUrl': self.get_product_url(tour_details),  # 'praga-express',
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
    @staticmethod
    def get_tour_details(tour) -> list:
        data = {
            'Parametry': [
                {
                    'Id': tour['Id'],
                    'Cena': tour['Cena'],
                    'CenaBezPromocji': tour['CenaBezPromocji'],
                    'CenyZaOsoby': [
                        {},
                        {},
                    ],
                    'Params': tour['Params'],
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
        return response.json()[0]

    @staticmethod
    def get_product_url(tour_details) -> str:
        google_url = tour_details['BazoweInformacje']['OfertaURLDlaGoogle'].split('/')
        logging.info(google_url)
        #TODO: check if index exist
        return google_url[1]

    @staticmethod
    def get_hotel_url(tour_details) -> str:
        google_url = tour_details['BazoweInformacje']['OfertaURLDlaGoogle'].split('/')
        logging.info(google_url)
        #TODO: check if index exist
        return google_url[2]

    def merge_tours(self) -> list:
        page_number = 0
        count_results = 1
        results = list()
        while count_results > 0:
            page_number += 1
            response = self.get_tours_list('objazd', page_number, limit=10)
            result = response['Wynik']
            count_results = len(result)
            results.extend(result)
        return results

    @staticmethod
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


#TODO: this should be inside Rainbow class
def main_rainbow(save_to_json: bool) -> None:
    scraper = RainbowScraper()
    tours = scraper.merge_tours()

    for tour in tours:
        logging.info(tour)
        try:
            tour_details = scraper.get_tour_details(tour)
            merged_tour_details = {
                "Tour": tour,
                "TourDetails": tour_details,
                "Prices": scraper.get_prices(tour_details)
            }
        except:
            logging.error("ERROR WITH TOUR:", tour)
            continue

        if save_to_json:
            #save_json_to_file('Rainbow', merged_tour_details, scraper.get_product_url(tour_details))
            save_json_to_gz_file('Rainbow', merged_tour_details, scraper.get_product_url(tour_details))

        tour_obj = RainbowParser(merged_tour_details).create_tour()


    if save_to_json:
        # save_json_to_file('Rainbow', tours, f'all-results')
        save_json_to_gz_file('Rainbow', tours, f'all-results')


