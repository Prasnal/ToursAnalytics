from typing import List
from dataclasses import dataclass
from typing import Optional
class TermsDetails:
    def __init__(self, term_start, term_end, term_price, nights, approved, length):
        self.term_start = term_start
        self.term_end = term_end
        self.term_price = term_price
        self.nights = nights
        self.approved = approved
        self.length = length

    def date_validator(self):
        pass

@dataclass
class Tour:
    tour_agency: str
    tour_agency_url: str

    tour_name: str
    countries: list
    tour_type: str
    tour_url: str
    klucz_omnibus: str

    tour_id: int
    terms_and_prices: List[TermsDetails]
    start_locations: list
    #TODO: last minute?

    grade: Optional[float] = None
    photos: Optional[list] = None

    #active_scraper
    #last_scraped_date
