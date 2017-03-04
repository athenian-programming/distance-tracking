import logging
import socket
import time
from threading import Event

import grpc
from grpc_support import GenericClient
from grpc_support import TimeoutException

from gen.grpc_server_pb2 import ClientInfo
from gen.grpc_server_pb2 import DistanceServerStub

logger = logging.getLogger(__name__)


class DistanceClient(GenericClient):
    def __init__(self, hostname):
        super(DistanceClient, self).__init__(hostname, "distance client")
        self.__ready = Event()
        self.__id = -1
        self.__ts = -1
        self.__distance = -1

    def _mark_ready(self):
        self.__ready.set()

    def _get_values(self, pause_secs=2.0):
        channel = grpc.insecure_channel(self._hostname)
        stub = DistanceServerStub(channel)
        while not self.stopped:
            logger.info("Connecting to gRPC server at {0}...".format(self._hostname))
            try:
                client_info = ClientInfo(info="{0} client".format(socket.gethostname()))
                server_info = stub.registerClient(client_info)
            except BaseException as e:
                logger.error("Failed to connect to gRPC server at {0} [{1}]".format(self._hostname, e))
                time.sleep(pause_secs)
                continue

            logger.info("Connected to gRPC server at {0} [{1}]".format(self._hostname, server_info.info))
            try:
                for val in stub.getDistances(client_info):
                    with self.value_lock:
                        self.__id = val.id
                        self.__ts = val.ts
                        self.__distance = val.distance
                    self._mark_ready()
            except BaseException as e:
                logger.info("Disconnected from gRPC server at {0} [{1}]".format(self._hostname, e))
                time.sleep(pause_secs)

    # Blocking
    def get_distance(self, timeout=None):
        while not self.stopped:
            if not self.__ready.wait(timeout):
                raise TimeoutException
            with self.value_lock:
                if self.__ready.is_set() and not self.stopped:
                    self.__ready.clear()
                    return {"id": self.__id, "ts": self.__ts, "distance": self.__distance}
