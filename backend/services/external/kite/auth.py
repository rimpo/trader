from injector import inject
from kiteconnect import KiteConnect
from lib import log

class AccessTokenService:
    """ Kite authentication service"""

    @inject
    def __init__(self, logger: log.Logger, kite: KiteConnect):
        self.__kite = kite
        self.__logger = logger

    def generate_access_token(self, request_token, api_secret) -> str:
        # TODO: renew access token logic
        data = self.__kite.generate_session(request_token, api_secret)
        return data["access_token"]


    def set_access_token(self, access_token):
        self.__kite.set_access_token(access_token)
        self.__logger.info("access_token generated!!")


