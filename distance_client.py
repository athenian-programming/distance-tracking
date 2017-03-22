import logging
import socket
import time

from grpc_support import CannotConnectException, SingleValueClient
from utils import setup_logging

from impl.grpc_distance_client import GrcpDistanceClient

logger = logging.getLogger(__name__)


class DistanceClient(SingleValueClient):
    def __init__(self, hostname):
        super(DistanceClient, self).__init__(hostname, desc="{0} client".format(socket.gethostname()))
        self.__grpc_client = GrcpDistanceClient(self.hostname)

    def _get_values(self, pause_secs=2.0):
        while not self.stopped:
            try:
                self.__grpc_client.connect()
            except CannotConnectException:
                time.sleep(pause_secs)
                continue

            try:
                for val in self.__grpc_client.values():
                    with self.value_lock:
                        self.currval = val
                    self._mark_ready()
                    if self.stopped:
                        break
            except BaseException as e:
                logger.info("Error reading values from gRPC server at {0} [{1}]".format(self.hostname, e))
                time.sleep(pause_secs)
            logger.info("Disconnected from gRPC server at {0}".format(self.hostname))

    def resetElapsed(self):
        self.__grpc_client.resetElapsed()


if __name__ == "__main__":
    setup_logging()
    print("Starting...")
    with DistanceClient("localhost") as client:
        for d, i in zip(client.values(), range(10)):
            print(d)
            if i % 5 == 0:
                client.resetElapsed()

        for i in range(10):
            print(client.value())
    print("Exiting...")
