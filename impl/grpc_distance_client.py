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


class GrcpDistanceClient(object):
    def __init__(self, hostname):
        self.__url = grpc_url(hostname)
        channel = grpc.insecure_channel(self.__url)
        self.__stub = DistanceServerStub(channel)
        self.__client_info = ClientInfo(info="{0} client".format(socket.gethostname()))
        self.__server_info = None

    @property
    def server_info(self):
        return self.__server_info

    def connect(self):
        logger.info("Connecting to gRPC server at {0}...".format(self.__url))
        try:
            self.__server_info = self.__stub.registerClient(self.__client_info)
        except BaseException as e:
            logger.error("Failed to connect to gRPC server at {0} [{1}]".format(self.__url, e))
            raise CannotConnectException(self.__url)

        logger.info("Connected to gRPC server at {0} [{1}]".format(self.__url, self.__server_info.info))

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def resetElapsed(self):
        self.__stub.resetElapsed(Empty())

    def value(self):
        return self.__stub.getDistance(Empty())

    def values(self):
        return self.__stub.getDistances(self.__client_info)


if __name__ == "__main__":
    setup_logging()

    with GrcpDistanceClient("localhost") as distances:
        for i in range(10):
            logger.info("Read value:\n{0}".format(distances.value()))

        for val in distances.values():
            logger.info("Read value:\n{0}".format(val))

    logger.info("Exiting...")
