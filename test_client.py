#!/usr/bin/env python3

import argparse
import logging
from threading import Thread

from utils import setup_logging

from distance_client import DistanceClient
from http_distance_client import HttpDistanceClient

logger = logging.getLogger(__name__)


def run_distance_client(repeat, size, print_vals):
    cnt = 0
    for i in range(repeat):
        print("Iteration {0}".format(i))
        with DistanceClient("localhost") as client:
            for d, j in zip(client.values(), range(size)):
                if print_vals:
                    print(d)
                cnt += 1

            for j in range(size):
                if print_vals:
                    print(client.value())
                cnt += 1

    assert (cnt == repeat * size * 2)


def run_http_distance_client(repeat, size, print_vals):
    cnt = 0

    for i in range(repeat):
        print("Iteration {0}".format(i))
        with HttpDistanceClient("localhost:8080") as client:
            for d, j in zip(client.values(), range(size)):
                if print_vals:
                    print(d)
                cnt += 1

            for j in range(size):
                if print_vals:
                    print(client.value())
                cnt += 1

    assert (cnt == repeat * size * 2)


if __name__ == "__main__":
    setup_logging()

    parser = argparse.ArgumentParser()
    parser.add_argument("--threads", type=int, default=1, help="Thread count")
    parser.add_argument("--repeat", type=int, default=1, help="Repeat count")
    parser.add_argument("--size", type=int, default=10, help="Sample size")
    parser.add_argument("--print_vals", default=False, action="store_true", help="Print values")
    args = vars(parser.parse_args())

    repeat = args["repeat"]
    size = args["size"]
    print_vals = args["print_vals"]

    for t in range(args["threads"]):
        Thread(target=run_distance_client, args=(repeat, size, print_vals)).start()
        Thread(target=run_http_distance_client, args=(repeat, size, print_vals)).start()

    print("Exiting...")
