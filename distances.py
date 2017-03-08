import logging
import socket

import grpc
from grpc_support import CannotConnectException
from grpc_support import grpc_url
from utils import setup_logging

from gen.grpc_server_pb2 import ClientInfo
from gen.grpc_server_pb2 import DistanceServerStub

logger = logging.getLogger(__name__)


class Distances(object):
    def __init__(self, hostname):
        url = grpc_url(hostname)
        try:
            channel = grpc.insecure_channel(url)
            self._stub = DistanceServerStub(channel)
            self._client_info = ClientInfo(info="{0} client".format(socket.gethostname()))
            self._server_info = self._stub.registerClient(self._client_info)
        except grpc._channel._Rendezvous:
            raise CannotConnectException(url)

    def values(self):
        return self._stub.getDistances(self._client_info)


if __name__ == "__main__":
    setup_logging()
    for val in Distances("127.0.0.1").values():
        logger.info("Read value:\n{0}".format(val))
    logger.info("Exiting...")
