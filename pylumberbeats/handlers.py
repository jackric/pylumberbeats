import datetime
import logging

from .client import LumberjackClient


_TIME_FORMAT = "%Y-%m-%dT%H:%M:%S"  # Logstash/Golang parsable

class LumberjackHandler(logging.Handler):
    """
    Logging handler for pushing log events Logstash
    """
    def __init__(self, host, port):
        logging.Handler.__init__(self)
        self._client = LumberjackClient(host, port)
        self._client.connect()

    def close(self):
        self._client.close()

    def emit(self, record):
        """
        Emit a record.

        If the stream was not opened because 'delay' was specified in the
        constructor, open it before calling the superclass's emit.
        """
        event = {
            "@timestamp": datetime.datetime.utcfromtimestamp(record.created).strftime(_TIME_FORMAT),
            "message": self.format(record),
            "python.lineno": record.lineno,
            "python.level": record.levelname,
            "python.filename": record.filename,
            "python.funcName": record.funcName
        }
        events = [event]
        self._client.send(events)
