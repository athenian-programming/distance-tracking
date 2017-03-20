import logging
import socket

import grpc
from google.protobuf.empty_pb2 import Empty
from grpc_support import CannotConnectException
from grpc_support import grpc_url
from utils import setup_logging

from pb.distance_server_pb2 import ClientInfo
from pb.distance_server_pb2 import DistanceServerStub

logger = logging.getLogger(__name__)


class DistanceClient(object):
    def __init__(self, hostname):
        url = grpc_url(hostname)
        channel = grpc.insecure_channel(url)
        self.__stub = DistanceServerStub(channel)
        self.__client_info = ClientInfo(info="{0} client".format(socket.gethostname()))
        self.__empty = Empty()
        try:
            self.__server_info = self.__stub.registerClient(self.__client_info)
        except grpc._channel._Rendezvous:
            raise CannotConnectException(url)
        logger.info("Connected to gRPC server at {0} [{1}]".format(url, self.__server_info.info))

    def get_value(self):
        return self.__stub.getDistance(self.__empty)

    def get_values(self):
        return self.__stub.getDistances(self.__client_info)


if __name__ == "__main__":
    setup_logging()

    distances = DistanceClient("localhost")

    for i in range(10):
        logger.info("Read value:\n{0}".format(distances.get_value()))

    for val in distances.get_values():
        logger.info("Read value:\n{0}".format(val))

    logger.info("Exiting...")
