#!/usr/bin/env python3
import argparse

import cli_args as cli

from http_distance_client import HttpDistanceClient

# Run this with python3 to get print() to flush properly

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--url", dest="url", default="localhost:8080", help="Distance server URL")
    parser.add_argument("-f", "--file", dest="file", required=True, help="CSV filename")
    cli.verbose(parser),
    args = vars(parser.parse_args())

    print("Starting...")
    with open(args["file"], 'w') as f, HttpDistanceClient(args["url"]) as client:
        for i in range(10):
            dist = client.value()
            val = "{0}, {1}".format(dist.elapsed, dist.distance)
            f.write(val + "\n")
            print(val)
    print("Exited...")
