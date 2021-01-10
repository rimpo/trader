import logging
import flask
from injector import Injector, Binder, Module, provider, noscope, singleton as singleton_scope
# from injector import Binder, Module, multiprovider, noscope, provider
from kiteconnect import KiteConnect

from lib.config import env, config
from lib import log

def configure(binder: Binder):
    pass

class Container(Module):

    @provider
    @singleton_scope
    def provide_kite_connect(self) -> KiteConnect:
        return KiteConnect(api_key=env.KITE_API_KEY)

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

