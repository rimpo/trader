from kiteconnect import KiteConnect
from lib import log

class AuthService:
    """ Kite authentication service"""
    def __init__(self, logger: log.Logger, kite: KiteConnect):
        self.__kite = kite
        self.__access_token = None
        self.__logger = logger

    def generate_access_token(self, request_token, api_secret) -> str:
        # TODO: renew access token logic
        if self.__access_token is None:
            data = self.__kite.generate_session(self.__request_token, api_secret)
            self.__access_token = data["access_token"]
            self.__kite.set_access_token(self.__access_token)
            self.__logger.info("access_token generated!!")
        return self.__access_token


