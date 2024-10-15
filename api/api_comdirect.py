import requests
import re
from bs4 import BeautifulSoup
from .api_provider import apiProvider

class apiComdirect(apiProvider):
    BASE_URL = "https://www.comdirect.de/inf/aktien/"

    ISIN_PRICE_PATTERN = re.compile(
            r"Typ:\s*(?P<Typ>\w+),\s*"  # Placeholder for Typ
            r"WKN:\s*(?P<WKN>[A-Z0-9]{6}),\s*"  # Placeholder for WKN
            r"ISIN:\s*(?P<ISIN>[A-Z0-9]+),\s*"  # Placeholder for ISIN
            r"Börse:\s*(?P<Börse>\w+),\s*"  # Placeholder for Börse
            r"Kurs:\s*(?P<Kurs>\d{1,5},\d{2})(?P<Currency>\s*[$€]|\s*[A-Za-z]{3}),\s*"  # Placeholder for Kurs (number) and Currency
            r"Stand:\s*vom\s*(?P<Stand>[\d.]+\s+\d{2}:\d{2})"  # Placeholder for Stand (date and time)
    )

    def __init__(self, logger):
        super().__init__(logger)
        self.provider = "Comdirect"       

    def get_price_isin_by_provider(self,isin):
        url = self.get_isin_url(isin)
        soup = self.get_soup(url)
        # Find the first <meta> tag with itemprop="description"
        meta_tag = soup.find('meta', attrs={'itemprop': 'description'})
        if meta_tag:
            # Search for the pattern in the content attribute
            match = self.ISIN_PRICE_PATTERN.search(meta_tag['content'])
            if match:
                # Extract the matched groups
                typ = match.group('Typ')
                wkn = match.group('WKN')
                isin_new = match.group('ISIN')
                boerse = match.group('Börse')
                kurs = match.group('Kurs')
                currency = self.format_currency(match.group('Currency'))
                if isin == isin_new:
                    return 200, kurs, currency
        raise self.IsinNotFoundException(isin=isin, provider=self.provider)

