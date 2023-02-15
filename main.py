import logging
import selectors
import socket
import sys
from enum import Enum

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(
    logging.StreamHandler(
        stream=sys.stdout
    )
)


class Default(Enum):
    HOST: str = ''
    PORT: int = 8000


def main(host: str | None = None, port: int | None = None):
    if host is None:
        host: str = Default.HOST.value
    if port is None:
        port: int = Default.PORT.value

    with selectors.SelectSelector() as selector:
        with socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM) as server_socket:
            server_socket.setsockopt(
                socket.SOL_SOCKET,
                socket.SO_REUSEADDR,
                True
            )

            server_socket.bind((host, port))
            server_socket.listen()
            server_socket.setblocking(False)

            logger.info('Server socket startup on port: %s', port)

            selector.register(
                server_socket,
                selectors.EVENT_READ,
                # accept_new_connection,
            )


if __name__ == "__main__":
    main()
