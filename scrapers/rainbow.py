import requests
import logging
import sys
sys.path.insert(0,'/home/krasnal/Projects/my_projects/ToursAnalytics/scraper') #TODO: change this
from tours.tour import Tour, TermsDetails
from utils.utils import save_json_to_gz_file

DIR = '/home/krasnal/Projects/my_projects/ToursAnalytics/scraper'  # TODO: move to settings

# TODO: download "odpoczynek" as well
# TODO: create settings with DIR and logging
# TODO: create class RainbowToursScraper
# TODO: add exceptions and validations
# TODO: add tests

# trip_type = 'objazd'


class RainbowParser:
    def __init__(self, tour_json):
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
def main_rainbow(save_to_json: bool) -> dict:
    scraper = RainbowScraper()
    tours = scraper.merge_tours()
    tours_data = dict()

    for tour in tours[:3]: #TODO: remove
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

        path = None
        if save_to_json:
            path = save_json_to_gz_file('Rainbow', merged_tour_details, scraper.get_product_url(tour_details))

        tour_obj = RainbowParser(merged_tour_details).create_tour()
        tours_data[tour_obj.tour_name] = {'path': path, 'tour_obj': tour_obj} #TODO: path and timestamp should be in the obj as well?

    if save_to_json:
        save_json_to_gz_file('Rainbow', tours, f'all-results')

    return tours_data