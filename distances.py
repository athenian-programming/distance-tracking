import logging
import socket

import grpc
from constants import GRPC_PORT_DEFAULT
from grpc_support import CannotConnectException

from gen.grpc_server_pb2 import ClientInfo
from gen.grpc_server_pb2 import DistanceServerStub

logger = logging.getLogger(__name__)


class Distances(object):
    def __init__(self, hostname):
        url = hostname if ":" in hostname else hostname + ":{0}".format(GRPC_PORT_DEFAULT)
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
    distances = Distances("127.0.0.1")
    for val in distances.values():
        print("Read distance:\n{0}".format(val))

    print("Disconnected from gRPC server")
