#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import socket

import grpc
from google.protobuf.empty_pb2 import Empty
from grpc_support import CannotConnectException
from grpc_support import grpc_url
from utils import setup_logging

from proto.distance_service_pb2 import ClientInfo
from proto.distance_service_pb2 import DistanceServiceStub

logger = logging.getLogger(__name__)


class GrcpDistanceClient(object):
    def __init__(self, hostname):
        self.__url = grpc_url(hostname)
        channel = grpc.insecure_channel(self.__url)
        self.__stub = DistanceServiceStub(channel)
        self.__client_info = ClientInfo(info="{0} client".format(socket.gethostname()))
        self.__server_info = None

    @property
    def server_info(self):
        return self.__server_info

    def connect(self):
        logger.info("Connecting to gRPC server at %s...", self.__url)
        try:
            self.__server_info = self.__stub.registerClient(self.__client_info)
            logger.info("Connected to gRPC server at %s [%s]", self.__url, self.__server_info.info)
        except BaseException as e:
            logger.error("Failed to connect to gRPC server at %s [%s]", self.__url, e)
            raise CannotConnectException(self.__url)

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        return self

    def value(self):
        return self.__stub.getDistance(Empty())

    def values(self):
        return self.__stub.getDistances(self.__client_info)


def main():
    setup_logging()

    with GrcpDistanceClient("localhost") as client:
        for i in range(10):
            logger.info("Read value:\n%s", client.value())
        for d, i in zip(client.values(), range(10)):
            logger.info("Read value:\n%s", d)

    logger.info("Exiting...")


if __name__ == "__main__":
    main()
