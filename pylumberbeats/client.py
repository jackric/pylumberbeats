import json
import struct
import socket

CODE_VERSION = '2'
CODE_WINDOW_SIZE = 'W'
CODE_JSON_DATAFRAME = 'J'
CODE_COMPRESSED = 'C'
CODE_ACK = 'A'

def _serialize(data):
    """
    Encode the list `data` in the lumberjack binary format.

    This function generates bitstring chunks, for efficient string production
    and to be easily pluggable into different concurrency frameworks (Twisted, gevent etc).
    """
    yield CODE_VERSION + CODE_WINDOW_SIZE + struct.pack('>I', len(data))
    for sequence_num, datum in enumerate(data, 1):
        yield CODE_VERSION + CODE_JSON_DATAFRAME + struct.pack('>I', sequence_num)
        encoded = json.dumps(datum)
        yield struct.pack('>I', len(encoded)) + encoded


class LumberjackClient(object):
    def __init__(self, host, port):
        self._host = host
        self._port = port
        self._sock = None

    def connect(self):
        s = socket.socket(socket.AF_INET)
        s.connect((self._host, self._port))
        self._sock = s

    def close(self):
        self._sock.close()

    def send(self, events):
        """
        Synchronously send the list `events` to Logstash. Each event is a dict-like object that will
        be serialized to JSON. Arbitrary fields may be sent, but it is recommended to conform to schemas
        used by Filebeat: https://www.elastic.co/guide/en/beats/filebeat/current/exported-fields.html
        """
        for frame in _serialize(events):
            self._sock.send(frame)
        ack_frame = self._sock.recv(6)
        assert ack_frame[0:2] == "2A"
        acked_events, = struct.unpack(">I", ack_frame[2:])
        assert acked_events == len(events)
