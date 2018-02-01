#!/usr/bin/env python3
import argparse

import arc852.cli_args as cli

from http_distance_client import HttpDistanceClient

# Run this with python3 to get print() to flush properly

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--url", dest="url", default="localhost:8080", help="Distance server URL")
    parser.add_argument("-f", "--file", dest="file", required=True, help="CSV filename")
    cli.log_level(parser)
    args = vars(parser.parse_args())

    print("Starting...")
    with open(args["file"], 'w') as f, HttpDistanceClient(args["url"]) as client:
        init_time = None
        for i in range(10):
            dist = client.value()
            if not init_time:
                init_time = dist.ts
            val = "{0}, {1}".format(dist.ts - init_time, dist.distance)
            f.write(val + "\n")
            print(val)
    print("Exited...")
