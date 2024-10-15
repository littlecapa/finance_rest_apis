from .api_comdirect import apiComdirect
from .api_alle_aktien import apiAlleAktien
from fastapi import HTTPException

class apiManager:
    def __init__(self, logger):
        self.api_comdirect = apiComdirect(logger)
        self.api_alle_aktien = apiAlleAktien(logger)
        self.logger = logger

    def get_price_isin(self,isin):
        try:
            price, currency = self.api_comdirect.get_price_isin(isin)
        except self.api_comdirect.IsinNotFoundException as e:
            self.logger.log_error(status=404, error_message=e.detail, exit_function = True)
            try:
                price, currency = self.api_alle_aktien.get_price_isin(isin)
            except self.api_comdirect.IsinNotFoundException as e:
                self.logger.log_error(status=404, error_message=e.detail, exit_function = True)
                raise HTTPException(status_code=404, detail=f"ISIN {isin} not found")

        return price, currency