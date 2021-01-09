import os
import logging
from datetime import datetime
from pythonjsonlogger import jsonlogger

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

    if os.environ.get('LOG_AS_JSON', '1') == '1':
        formatter = CustomJsonFormatter('%(timestamp)s %(level)s %(name)s %(message)s %(module)s %(lineno)s')
        handler.setFormatter(formatter)

    logger.addHandler(handler)
