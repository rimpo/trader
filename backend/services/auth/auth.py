from kiteconnect import KiteConnect
from lib import log
from typing import Protocol
from injector import inject


class AuthRepository(Protocol):
    def create_auth(self, request_token: str, access_token: str):
        pass

    def get_auth(self) -> dict:
        pass


class AuthServiceBase(Protocol):
    def get_kite(self):
        pass


class AuthService:
    @inject
    def __init__(self, logger: log.Logger, kite: KiteConnect, api_secret: str, auth_repo: AuthRepository):
        self.__logger = logger
        self.__api_secret = api_secret
        self.__kite = kite
        self.__auth_repo = auth_repo
        self.__access_token = ''
        result = self.__auth_repo.get_auth()
        if result is not None:
            self.__kite.set_access_token(result["access_token"])
            self.__access_token = result["access_token"]
            logger.info("-------------------- set access token ------------------")

    def generate_access_token(self, request_token: str):
        # TODO: renew access token logic
        data = self.__kite.generate_session(request_token, self.__api_secret)
        self.__logger.info(f"data:{data}")
        self.__access_token = data["access_token"]
        self.__auth_repo.create_auth(request_token, self.__access_token)

    def get_access_token(self):
        return self.__access_token

    def get_kite(self):
        return self.__kite

    def renew_access_token(self):
        data = self.__kite.renew_access_token('', self.__api_secret)
        self.__logger.info(f"{data}")

