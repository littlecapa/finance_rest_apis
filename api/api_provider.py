import requests
import re
from bs4 import BeautifulSoup

class apiProvider:
    BASE_URL = ""

    ISIN_PRICE_PATTERN = None

    def __init__(self, logger):
        self.provider = ""
        self.logger = logger

    class IsinNotFoundException(Exception):
        def __init__(self, isin, provider):
            self.status = 404
            self.isin = isin
            self.provider = provider
            self.detail = f"Error {self.status}: Provider {provider} could not find ISIN {self.isin}"
            super().__init__(self.detail)  # Pass the error message to the base Exception class

    class InvalidCurrencyException(Exception):
        def __init__(self, currency):
            status = 500
            detail = f"Error {status}: Invalid Currency #{currency}#"
            self.logger.log_error(status, detail)
            super().__init__(status_code=status, detail=detail)

    def is_valid_currency(self, currency):
        # Check if the currency is exactly 3 characters long and all are uppercase
        return len(currency) == 3 and currency.isupper()

    def format_currency(self, currency):
        if currency is None or currency == '':
            return "EUR"
        currency = currency.lstrip().rstrip().upper()
        if currency == "€":
            return "EUR"
        elif currency == "$":
            return "USD"
        if not self.is_valid_currency(currency):
            raise self.InvalidCurrencyException(currency)
        return currency
    
    def get_isin_url(self, isin):
        return self.BASE_URL + isin
    
    def get_soup(self, url):
        response = requests.get(url)
        response.encoding = 'utf-8'
        return BeautifulSoup(response.content, "html.parser")
    
    def get_price_isin_by_provider(self,isin):
        raise Exception("get_price_isin_by_provider not implemented")
    
    def get_price_isin(self,isin):
        self.logger.start_execution(f"/stock_price_isin/{self.provider}")
        status, kurs, currency = self.get_price_isin_by_provider(isin)
        self.logger.log_execution(f"/stock_price_isin/{self.provider}", status = status, isin=isin)
        return kurs, currency