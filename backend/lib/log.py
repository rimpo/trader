import os
import logging
from datetime import datetime
from pythonjsonlogger import jsonlogger


class CustomFormatter(logging.Formatter):
    """Logging Formatter to add colors and count warning / errors"""

    grey = "\x1b[38;21m"
    yellow = "\x1b[33;21m"
    red = "\x1b[31;21m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)"

    FORMATS = {
        logging.DEBUG: grey + format + reset,
        logging.INFO: grey + format + reset,
        logging.WARNING: yellow + format + reset,
        logging.ERROR: red + format + reset,
        logging.CRITICAL: bold_red + format + reset
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


class CustomJsonFormatter(jsonlogger.JsonFormatter):
    def add_fields(self, log_record, record, message_dict):
        super(CustomJsonFormatter, self).add_fields(log_record, record, message_dict)
        if not log_record.get('timestamp'):
            now = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%fZ')
            log_record['timestamp'] = now

        if log_record.get('level'):
            log_record['level'] = log_record['level'].upper()
        else:
            log_record['level'] = record.levelname

class LoggerAdapter(logging.LoggerAdapter):
    def process(self, msg, kwargs):
        if isinstance(self.logger, logging.LoggerAdapter):
            msg, kwargs = self.logger.process(msg, kwargs)

        kwargs.setdefault('extra', {})

        kwargs["extra"].update(self.extra)
        return msg, kwargs

class Logger(LoggerAdapter):
    pass


def initialize_root_logger():
    logger = logging.getLogger()

    level = os.getenv('LOG_LEVEL', 'warning')
    logger.setLevel(logging.getLevelName(level.upper()))

    handler = logging.StreamHandler()

    if os.environ.get('LOG_AS_JSON', '0') == '1':
        formatter = CustomJsonFormatter('%(timestamp)s %(level)s %(name)s %(message)s %(module)s %(lineno)s')
        handler.setFormatter(formatter)
    else:
        handler.setFormatter(CustomFormatter())

    logger.addHandler(handler)
