import requests
import re
from bs4 import BeautifulSoup
from .api_provider import apiProvider

class apiAlleAktien(apiProvider):
    BASE_URL = "https://www.alleaktien.com/data/"

    PRICE_PATTERN = r'(?P<price>\d{1,3},\d{2})'  # Matches price like '22,82'
    CURRENCY_PATTERN = r'(?P<currency>[A-Za-z]{3}|\$|€)'  # Matches currency like 'EUR', '$', '€'
    PRICE_CURRENCY_PATTERN = rf'({PRICE_PATTERN})\s*({CURRENCY_PATTERN})'

    # Combine the patterns for the full match
    ISIN_PRICE_PATTERN = rf'class="whitespace-nowrap live-quote flex flex-row price text-black"><div>{PRICE_CURRENCY_PATTERN}'

    def __init__(self, logger):
        super().__init__(logger)
        self.provider = "Alle Aktien"

    def get_price_isin_by_provider(self,isin):
        url = self.get_isin_url(isin)
        soup = self.get_soup(url)
        not_found = soup.find('h1', class_="error-page--headline headline headline--h1")
        if not_found == None:
            print("Gefunden")
            match = re.search(self.ISIN_PRICE_PATTERN, str(soup))
            if match:
                print("Match")
                price = match.group('price')
                currency = self.format_currency(match.group('currency'))
                return 200, price, currency
        raise self.IsinNotFoundException(isin=isin, provider=self.provider)