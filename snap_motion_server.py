#!/usr/bin/env python

import argparse
import logging
from threading import Lock

import cli_args as cli
from constants import SERIAL_PORT, BAUD_RATE, LOG_LEVEL, DEVICE_ID
from flask import Flask
from flask import make_response
from serial_reader import SerialReader
from utils import setup_logging

logger = logging.getLogger(__name__)

CALIBRATION_BY_VALUES = "9-DOF Sensor calibrated by values"
CALIBRATION_BY_LOG = "9-DOF Sensor calibrated by log"
CALIB_PUBLISH = "calib_publish"
PUBLISH_LOCK = "publish_lock"

calibrated_by_values = False
calibrated_by_log = False
curr_x = 0
curr_y = 0
curr_z = 0
curr_calib = ""

flask = Flask(__name__)


@flask.route("/x")
def x():
    return response(curr_x)


@flask.route("/y")
def y():
    return response(curr_y)


@flask.route("/z")
def z():
    return response(curr_z)


@flask.route("/calib")
def calib():
    return response(curr_calib)


def response(val):
    resp = make_response(str(val), 200)
    resp.headers["Content-Type"] = "text/plain"
    resp.headers["Access-Control-Allow-Origin"] = "http://snap.berkeley.edu"
    resp.headers["Access-Control-Allow-Methods"] = "GET, POST"
    return resp


# SerialReader calls this for every line read from Arduino
def fetch_data(val, userdata):
    global curr_x, curr_y, curr_z, curr_calib, calibrated_by_values, calibrated_by_log

    if "X:" not in val:
        logger.info("Non-data: %s", val)
    else:
        try:
            logger.info("Vals: %s", val)
            vals = val.split("\t")

            x_val = vals[0]
            curr_x = round(float(x_val.split(": ")[1]), 1)

            y_val = vals[1]
            curr_y = round(float(y_val.split(": ")[1]), 1)

            z_val = vals[2]
            curr_z = round(float(z_val.split(": ")[1]), 1)

            logger.info("x: %d, y: %d, z: %d", curr_x, curr_y, curr_z)

            if not calibrated_by_values:
                # The arduino sketch includes a "! " prefix to SYS if the data is not calibrated (and thus not reliable)
                if "! " in val:
                    nocalib_str = val[val.index("! "):]
                    logger.info("9-DOF Sensor not calibrated by log: %s", nocalib_str)
                    curr_calib = nocalib_str
                    calibrated_by_log = False
                else:
                    if not calibrated_by_log:
                        msg = CALIBRATION_BY_LOG
                        logger.info(msg)
                        curr_calib = msg
                        calibrated_by_log = True

                    calib_str = vals[3]
                    calibs = calib_str.split(" ")
                    sys_calib = int(calibs[0].split(":")[1])
                    gyro_calib = int(calibs[1].split(":")[1])
                    mag_calib = int(calibs[2].split(":")[1])
                    acc_calib = int(calibs[3].split(":")[1])

                    if sys_calib == 3 and gyro_calib == 3 and mag_calib == 3 and acc_calib == 3:
                        msg = CALIBRATION_BY_VALUES
                        logger.info(msg)
                        curr_calib = msg
                        calibrated_by_values = True
                    else:
                        curr_calib = calib_str
        except IndexError:
            logger.info("Formatting error: %s", val)


if __name__ == "__main__":
    # Parse CLI args
    parser = argparse.ArgumentParser()
    cli.device_id(parser)
    cli.serial_port(parser)
    cli.baud_rate(parser)
    cli.verbose(parser)
    args = vars(parser.parse_args())

    # Setup logging
    setup_logging(level=args[LOG_LEVEL])

    userdata = {PUBLISH_LOCK: Lock()},

    with SerialReader(func=fetch_data,
                      userdata=userdata,
                      port=SerialReader.lookup_port(args[DEVICE_ID]) if args.get(DEVICE_ID) else args[SERIAL_PORT],
                      baudrate=args[BAUD_RATE],
                      debug=True):
        try:
            flask.run(host="0.0.0.0", port=9000)
        except KeyboardInterrupt:
            pass

    logger.info("Exiting...")
