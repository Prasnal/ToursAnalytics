from typing import List

class TermsDetails:
    def __init__(self, term_start, term_end, term_price):
        self.term_start = term_start
        self.term_end = term_end
        self.term_price = term_price

class Tour:
    tour_agency: str
    tour_agency_url: str

    tour_name: str
    countries: list
    tour_type: str
    tour_url: str
    klucz_omnibus: str

    tour_id: int
    food_plans: list
    terms_and_prices: List[TermsDetails]
    start_locations: list
    #TODO: last minute?




    grade = float
    photos = list
    #active_scraper
    #last_scraped_date
