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
        self.__ready = Event()
        self.__currval = None

    def _mark_ready(self):
        self.__ready.set()

    def _get_values(self, pause_secs=2.0):
        while not self.stopped:
            try:
                self.__distance_client.connect()
            except CannotConnectException:
                time.sleep(pause_secs)
                continue

            try:
                for val in self.__distance_client.values():
                    with self.value_lock:
                        self.__currval = copy.deepcopy(val)
                    self._mark_ready()
                    if self.stopped:
                        break
            except BaseException as e:
                logger.info("Error reading values {0} [{1}]".format(self.hostname, e))
                time.sleep(pause_secs)
            logger.info("Disconnected from gRPC server at {0}".format(self.hostname))

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

    def values(self):
        while not self.stopped:
            yield self.value()


if __name__ == "__main__":
    setup_logging()

    print("Starting...")

    with DistanceClient("localhost") as client:
        for d, i in zip(client.values(), range(10)):
            print(d)
            if i % 5 == 0:
                client.resetElapsed()

    print("Exiting...")
