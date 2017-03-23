#!/usr/bin/env python

import argparse
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


if __name__ == "__main__":
    setup_logging()

    parser = argparse.ArgumentParser()
    parser.add_argument("--count", type=int, default=10, help="Count")
    args = vars(parser.parse_args())

    cnt = 0
    with DistanceClient("localhost") as client:
        for d, i in zip(client.values(), range(args["count"])):
            print(d)
            cnt += 1

        for i in range(args["count"]):
            print(client.value())
            cnt += 1

    assert (cnt == 2 * args["count"])

    print("Exiting...")
