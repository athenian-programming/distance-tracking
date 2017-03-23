#!/usr/bin/env python3

import json
import logging
import socket
import time

import requests
from grpc_support import SingleValueClient
from utils import setup_logging

logger = logging.getLogger(__name__)


class Distance(object):
    def __init__(self, id, ts, elapsed, distance):
        self.id = id
        self.ts = ts
        self.elapsed = elapsed
        self.distance = distance

    def __str__(self):
        return "id: {0}\nts: {1}\nelapsed: {2}\ndistance: {3}\n".format(self.id, self.ts, self.elapsed, self.distance)


class HttpDistanceClient(SingleValueClient):
    def __init__(self, hostname):
        super(HttpDistanceClient, self).__init__(hostname,
                                                 http_hostname=True,
                                                 desc="{0} client".format(socket.gethostname()))

    def _get_values(self, pause_secs=2.0):
        while not self.stopped:
            try:
                logger.info("Connecting to HTTP server at {0}...".format(self.hostname))
                response = requests.get(self.hostname + "/v1/distances", headers={"cache-control": "no-cache"},
                                        stream=True)
                logger.info("Connected to HTTP server at {0}".format(self.hostname))
            except BaseException as e:
                logger.error("Failed to connect to HTTP server at {0} [{1}]".format(self.hostname, e))
                time.sleep(pause_secs)
                continue

            try:
                for json_str in response.iter_lines():
                    val = json.loads(json_str)["result"]
                    with self.value_lock:
                        self.currval = Distance(id=int(val["id"]),
                                                ts=int(val["ts"]),
                                                elapsed=int(val["elapsed"]),
                                                distance=int(val["distance"]))
                    self._mark_ready()
                    if self.stopped:
                        break
            except BaseException as e:
                logger.info("Error reading values from HTTP server at {0} [{1}]".format(self.hostname, e))
                time.sleep(pause_secs)

            logger.info("Disconnected from HTTP server at {0}".format(self.hostname))


if __name__ == "__main__":
    setup_logging()
    cnt = 0
    with HttpDistanceClient("localhost:8080") as client:
        for d, i in zip(client.values(), range(10)):
            print(d)
            cnt += 1

        for i in range(10):
            print(client.value())
            cnt += 1

    assert (cnt == 20)
    print("Exiting...")
