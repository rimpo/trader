import logging
import flask
from injector import Injector, Binder, Module, provider, noscope, singleton as singleton_scope
# from injector import Binder, Module, multiprovider, noscope, provider
from kiteconnect import KiteConnect

from lib.config import env, config
from lib import log
from lib.telegram_bot import TelegramBot

from services import external
from services import auth, instruments, historical_data, order, strategy


def configure(binder: Binder):
    binder.bind(auth.AuthRepository, auth.Repository)

    binder.bind(instruments.ExternalInstrumentService, external.kite.InstrumentService)
    binder.bind(instruments.InstrumentService, instruments.InstrumentService)
    binder.bind(instruments.InstrumentRepository, instruments.Repository)

    binder.bind(historical_data.HistoricalDataService, historical_data.HistoricalDataService)
    binder.bind(historical_data.ExternalHistoricalDataService, external.kite.HistoricalDataService)
    binder.bind(historical_data.HistoricalDataRepository, historical_data.repo.Repository)

    binder.bind(order.ExternalPositionService, external.kite.order.PositionService)
    binder.bind(order.PositionService, order.PositionService)

    binder.bind(order.ExternalHoldingService, external.kite.order.HoldingService)
    binder.bind(order.HoldingService, order.HoldingService)
    binder.bind(order.PositionHoldingService, order.PositionHoldingService)

    binder.bind(order.ExternalMarketOrderServiceCNC, external.kite.order.MarketOrderService)
    binder.bind(order.MarketOrderServiceCNC, order.MarketOrderServiceCNC)

    binder.bind(order.ExternalMISMarketOrderService, external.kite.order.MarketOrderService)
    binder.bind(order.MISMarketOrderService, order.MISMarketOrderService)

    binder.bind(strategy.signal.SignalRepository, strategy.signal.repo.Repository)


class Container(Module):

    @provider
    @singleton_scope
    def provide_telegram_bot(self) -> TelegramBot:
        return TelegramBot(access_token=env.TRADER_RIMPO_BOT_ACCESS_TOKEN)

    @provider
    @singleton_scope
    def provide_kite(self, logger: log.Logger) -> KiteConnect:
        return KiteConnect(env.KITE_API_KEY)

    @provider
    @noscope
    def provide_access_token_service(self, logger: log.Logger, kite: KiteConnect) -> external.kite.AccessTokenService:
        return external.kite.AccessTokenService(logger, kite)

    @provider
    @singleton_scope
    def provide_auth_service(self, logger: log.Logger, kite: KiteConnect, auth_repo: auth.AuthRepository) -> auth.AuthService:
        return auth.AuthService(
            logger,
            kite,
            env.KITE_API_SECRET,
            auth_repo
        )

    @provider
    @singleton_scope
    def provide_logger(self) -> log.Logger:
        """Provides a logger scoped to the thread"""
        return log.Logger(logging.getLogger(), {})

    @provider
    @noscope
    def provide_config(self) -> config.Config:
        return config.Config(
            api_key=env.KITE_API_KEY,
            api_secret=env.KITE_API_SECRET
        )

    @provider
    @noscope
    def provide_instrument_service(self, logger: log.Logger, kite: KiteConnect) -> external.kite.InstrumentService:
        return external.kite.InstrumentService(logger, kite)
    """
    def provide_auth_user(self) -> lib.auth.user.User:
        if not hasattr(flask.g, 'current_user') or flask.g.current_user is None:
            raise Exception("flask.g.current_user is empty")

        if not isinstance(flask.g.current_user, lib.auth.user.User):
            raise Exception("unexpected value in g.current_user: {}".format(flask.g.current_user))

        return flask.g.current_user

    @provider
    @noscope
    def provide_local_primary_engine(self) -> LocalPrimaryEngine:
        return create_engine(get_database_uri())

    @provider
    @noscope
    def provide_odoo_replica_engine(self) -> OdooReplicaEngine:
        return create_engine(get_odoo_database_uri())"""


def create_injector() -> Injector:
    modules = [
        configure,
        Container,
    ]

    # if env.TRADER_ENV == env.DEVELOPMENT:
    #    modules.append(dev.dependencies.Container)
    # elif env.TRADER_ENV == env.TESTING:
    #    modules.append(test_dependencies.Container)

    return Injector(modules)

