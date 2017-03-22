#!/usr/bin/env python3
import argparse

from http_distance_client import HttpDistanceClient

# Run this with python3 to get print() to flush properly

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--url", dest="url", required=True, help="Distance server URL")
    parser.add_argument("-f", "--file", dest="file", required=True, help="CSV filename")
    args = vars(parser.parse_args())

    print("Starting...")
    with  open(args["file"], 'w') as file:
        for dist, i in zip(HttpDistanceClient(args["url"]).values(), range(10)):
            val = "{0}, {1}".format(dist.elapsed, dist.distance)
            file.write(val + "\n")
            print(val)
    print("Exited...")
