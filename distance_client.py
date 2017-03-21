import copy
import logging
import socket
import time
from threading import Event

from grpc_support import GenericClient, CannotConnectException
from grpc_support import TimeoutException
from utils import setup_logging

from impl.grpc_distance_client import GrcpDistanceClient

logger = logging.getLogger(__name__)


class DistanceClient(GenericClient):
    def __init__(self, hostname):
        super(DistanceClient, self).__init__(hostname, desc="{0} client".format(socket.gethostname()))
        self.__distance_client = GrcpDistanceClient(hostname)
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
            try:
                self.__distance_client.connect()
                self.__connected = True
            except CannotConnectException:
                time.sleep(pause_secs)
                continue

            try:
                for val in self.__distance_client.values():
                    with self.value_lock:
                        self.__currval = copy.deepcopy(val)
                    self._mark_ready()
            except BaseException as e:
                logger.info("Disconnected from gRPC server at {0} [{1}]".format(self.hostname, e))
                self.__connected = False
                time.sleep(pause_secs)

    def resetElapsed(self):
        self.__distance_client.resetElapsed()

    # Blocking
    def value(self, timeout=None):
        while not self.stopped:
            if not self.__ready.wait(timeout):
                raise TimeoutException
            with self.value_lock:
                if self.__ready.is_set() and not self.stopped:
                    self.__ready.clear()
                    return self.__currval


if __name__ == "__main__":
    setup_logging()

    with DistanceClient("localhost") as distances:
        for i in range(1000):
            logger.info("Read value:\n{0}".format(distances.value()))
            if i % 5 == 0:
                distances.resetElapsed()

    logger.info("Exiting...")
