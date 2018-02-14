#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import json
import logging
import socket
import time

import arc852.cli_args as cli
import requests
from arc852.constants import LOG_LEVEL
from arc852.grpc_support import SingleValueClient
from arc852.utils import setup_logging

logger = logging.getLogger(__name__)


class Distance(object):
    def __init__(self, id, ts, distance):
        self.id = id
        self.ts = ts
        self.distance = distance

    def __str__(self):
        return "id: {0}\nts: {1}\ndistance: {2}\n".format(self.id, self.ts, self.distance)


class HttpDistanceClient(SingleValueClient):
    def __init__(self, hostname):
        super(HttpDistanceClient, self).__init__(hostname,
                                                 http_hostname=True,
                                                 desc="{0} client".format(socket.gethostname()))

    def _get_values(self, pause_secs=2.0):
        while not self.stopped:
            try:
                logger.info("Connecting to HTTP server at %s...", self.hostname)
                response = requests.get(self.hostname + "/v1/distances",
                                        headers={"cache-control": "no-cache"},
                                        stream=True)
                logger.info("Connected to HTTP server at %s", self.hostname)
            except BaseException as e:
                logger.error("Failed to connect to HTTP server at %s [%s]", self.hostname, e)
                time.sleep(pause_secs)
                continue

            try:
                for json_str in response.iter_lines():
                    val = json.loads(json_str)["result"]
                    with self.value_lock:
                        self.currval = Distance(id=int(val["id"]),
                                                ts=int(val["ts"]),
                                                distance=int(val["distance"]))
                    self._mark_ready()
                    if self.stopped:
                        break
            except BaseException as e:
                logger.info("Error reading values from HTTP server at %s [%s]", self.hostname, e)
                time.sleep(pause_secs)

            logger.info("Disconnected from HTTP server at %s", self.hostname)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", dest="host", default="localhost:8080", help="Distance server hostname")
    cli.log_level(parser)
    args = vars(parser.parse_args())

    setup_logging(level=args[LOG_LEVEL])

    cnt = 0

    for i in range(5):
        print("Iteration {0}".format(i))
        with HttpDistanceClient(args["host"]) as client:
            for d, j in zip(client.values(), range(10)):
                print(d)
                cnt += 1

            for j in range(10):
                print(client.value())
                cnt += 1

    assert cnt == 5 * 10 * 2

    print("Exiting...")


if __name__ == "__main__":
    main()
