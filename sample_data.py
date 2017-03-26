#!/usr/bin/env python3
import argparse

import cli_args as cli

from http_distance_client import HttpDistanceClient

# Run this with python3 to get print() to flush properly

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--url", dest="url", required=True, help="Distance server URL")
    cli.verbose(parser),
    args = vars(parser.parse_args())

    print("Starting...")
    with HttpDistanceClient(args["url"]) as client:
        for i in range(10):
            print(client.value())
    print("Exited...")
