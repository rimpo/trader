from kiteconnect import KiteConnect
from models.auth import AuthModel
from lib import log


class AuthService:
    def __init__(self, logger: log.Logger, kite: KiteConnect, api_secret: str):
        self.__api_secret = api_secret
        self.__kite = kite
        self.__access_token = ''
        auth_info = AuthModel.objects().first()
        if auth_info is not None:
            self.__kite.set_access_token(auth_info.access_token)
            self.__access_token = auth_info.access_token
            logger.info("-------------------- set access token ------------------")

    def generate_access_token(self, request_token: str):
        # TODO: renew access token logic
        data = self.__kite.generate_session(request_token, self.__api_secret)
        self.__access_token = data["access_token"]
        AuthModel(request_token=request_token, access_token=self.__access_token).save()

    def get_access_token(self):
        return self.__access_token
