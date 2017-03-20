import copy
import logging
import socket
import time
from threading import Event

import grpc
from grpc_support import GenericClient
from grpc_support import TimeoutException
from utils import setup_logging

from pb.distance_server_pb2 import ClientInfo
from pb.distance_server_pb2 import DistanceServerStub

logger = logging.getLogger(__name__)


class DistanceClient(GenericClient):
    def __init__(self, hostname):
        super(DistanceClient, self).__init__(hostname, desc="{0} client".format(socket.gethostname()))
        channel = grpc.insecure_channel(self.hostname)
        self.__stub = DistanceServerStub(channel)
        self.__client_info = ClientInfo(info="{0} client".format(socket.gethostname()))
        self.__connected = False
        self.__ready = Event()
        self.__currval = None

    @property
    def connected(self):
        return self.__connected

    def _mark_ready(self):
        self.__ready.set()

    def _get_values(self, pause_secs=2.0):
        while not self.stopped:
            logger.info("Connecting to gRPC server at {0}...".format(self.hostname))

            try:
                server_info = self.__stub.registerClient(self.__client_info)
                self.__connected = True
            except BaseException as e:
                logger.error("Failed to connect to gRPC server at {0} [{1}]".format(self.hostname, e))
                time.sleep(pause_secs)
                continue
            logger.info("Connected to gRPC server at {0} [{1}]".format(self.hostname, server_info.info))

            try:
                for val in self.__stub.getDistances(self.__client_info):
                    with self.value_lock:
                        self.__currval = copy.deepcopy(val)
                    self._mark_ready()
            except BaseException as e:
                logger.info("Disconnected from gRPC server at {0} [{1}]".format(self.hostname, e))
                self.__connected = False
                time.sleep(pause_secs)

    # Blocking
    def get_value(self, timeout=None):
        while not self.stopped:
            if not self.__ready.wait(timeout):
                raise TimeoutException
            with self.value_lock:
                if self.__ready.is_set() and not self.stopped:
                    self.__ready.clear()
                    return self.__currval


if __name__ == "__main__":
    setup_logging()
    with DistanceClient("localhost") as client:
        for i in range(1000):
            logger.info("Read value:\n{0}".format(client.get_value()))
    logger.info("Exiting...")
