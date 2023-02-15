import logging
import selectors
import socket

logger = logging.getLogger(__name__)

_CHUNK_BYTES: int = 1024


class ClientConnection:

    @classmethod
    def accept(cls, selector: selectors.BaseSelector, sock: socket.socket):
        connection, address = sock.accept()
        logger.info('Accepted new client connetction: %s', address)

        connection.setblocking(False)

        selector.register(connection, selectors.EVENT_READ, cls._callback)

    @staticmethod
    def _callback(selector: selectors.BaseSelector, sock: socket.socket):
        data = sock.recv(_CHUNK_BYTES)
        if data:
            sock.send(data)
        else:
            logger.info('Closing connection: %s', sock)
            selector.unregister(sock)
            sock.close()
