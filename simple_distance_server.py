#!/usr/bin/env python

import argparse
import logging

import cli_args as cli
from constants import OOR_SIZE, OOR_TIME_DEFAULT, OOR_TIME, OOR_UPPER_DEFAULT, OOR_UPPER
from constants import SERIAL_PORT, BAUD_RATE, LOG_LEVEL, DEVICE_ID, OOR_SIZE_DEFAULT
from flask import Flask
from flask import make_response
from out_of_range_values import OutOfRangeValues
from prometheus_client import start_http_server
from serial_reader import SerialReader
from utils import setup_logging, waitForKeyboardInterrupt

logger = logging.getLogger(__name__)

OOR_VALUES = "oor_values"
OUT_OF_RANGE = "-1".encode("utf-8")


class DistanceServer(object):
    def __init__(self,
                 oor_size=OOR_SIZE_DEFAULT,
                 oor_time=OOR_TIME_DEFAULT,
                 oor_upper=OOR_UPPER_DEFAULT):
        self.__oor_values = OutOfRangeValues(size=oor_size)
        self.__oor_time = oor_time
        self.__oor_upper = oor_upper
        self.__currval = None

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()
        return self

    def start(self):
        flask = Flask(__name__)

        @flask.route("/distance")
        def distance():
            return response(self.__currval if self.__currval else -1)

        flask.run(host="0.0.0.0", port=9000)

    def stop(self):
        pass

    def fetch_data(self, val_str, userdata):
        # Values sometimes get compacted together, take the later value if that happens since it's newer
        if "\r" in val_str:
            val_str = val_str.split("\r")[1]

        mm = int(val_str)

        if self.__oor_upper > 0 and (mm <= 0 or mm > self.__oor_upper):
            # Filter out bad data
            self.__oor_values.mark()
            if self.__oor_values.is_out_of_range(self.__oor_time):
                self.__oor_values.clear()
                self.__currval = -1
        else:
            self.__currval = mm


def response(val=""):
    resp = make_response(str(val), 200)
    resp.headers["Content-Type"] = "text/plain"
    resp.headers["Access-Control-Allow-Origin"] = "http://snap.berkeley.edu"
    resp.headers["Access-Control-Allow-Methods"] = "GET, POST"
    return resp


if __name__ == "__main__":
    # Parse CLI args
    parser = argparse.ArgumentParser()
    cli.grpc_port(parser)
    cli.device_id(parser)
    cli.serial_port(parser)
    cli.baud_rate(parser)
    cli.oor_size(parser)
    cli.oor_time(parser)
    cli.oor_upper(parser)
    cli.verbose(parser)
    args = vars(parser.parse_args())

    # Setup logging
    setup_logging(level=args[LOG_LEVEL])

    # Start up a server to expose the metrics.
    start_http_server(8000)

    with DistanceServer(oor_size=args[OOR_SIZE],
                        oor_time=args[OOR_TIME],
                        oor_upper=args[OOR_UPPER]) as server:
        with SerialReader(func=server.fetch_data,
                          userdata=None,
                          port=SerialReader.lookup_port(args[DEVICE_ID] if args.get(DEVICE_ID) else args[SERIAL_PORT]),
                          baudrate=args[BAUD_RATE]):
            waitForKeyboardInterrupt()

    logger.info("Exiting...")
