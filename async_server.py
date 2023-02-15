import logging
import selectors
import socket
import sys

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(
    logging.StreamHandler(stream=sys.stdout),
)

_HOST, _PORT = '', 8000


def accept_new_connection(selector: selectors.BaseSelector, sock: socket.socket):
    new_connection, address = sock.accept()
    logger.info('Accepted new connection: %s', address)
    new_connection.setblocking(False)

    selector.register(new_connection, selectors.EVENT_READ, callback)


def callback(selector: selectors.BaseSelector, sock: socket.socket):
    default_bytes: int = 1024
    data = sock.recv(default_bytes)
    if data:
        sock.send(data)
    else:
        logger.info('Closing connection: %s', sock)
        selector.unregister(sock)
        sock.close()


def run_iteration(selector: selectors.BaseSelector):
    events = selector.select()
    for key, mask in events:
        callback = key.data
        callback(selector, key.fileobj)


def serve_forever():
    with selectors.SelectSelector() as selector:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.setsockopt(
                socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
            server_socket.bind((_HOST, _PORT))
            server_socket.listen()
            server_socket.setblocking(False)
            logger.info('Server started on port %s', _PORT)

            selector.register(
                server_socket, selectors.EVENT_READ, accept_new_connection)

            while True:
                run_iteration(selector)


if __name__ == '__main__':
    serve_forever()
