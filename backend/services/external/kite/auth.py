from kiteconnect import KiteConnect

class KiteAuthService:
    """Kite authentication service"""
    def __init__(self, api_key: str,  api_secret: str, request_token: str,):
        self.__kite = KiteConnect(api_key)
        data = self.__kite.generate_session(request_token, api_secret)
        self.__access_token = data["access_token"]

    def get_access_token(self) -> str:
        return self.__access_token


