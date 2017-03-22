#!/usr/bin/env python3

import json

import requests
from utils import add_http_prefix

from pb.distance_server_pb2 import Distance


class HttpDistanceClient(object):
    def __init__(self, url):
        self.__url = add_http_prefix(url)

    def values(self):
        request = requests.get(self.__url, headers={"cache-control": "no-cache"}, stream=True)
        for json_str in request.iter_lines():
            val = json.loads(json_str)["result"]
            # python3 doesn't have long(), just int()
            yield Distance(id=int(val["id"]),
                           ts=int(val["ts"]),
                           elapsed=int(val["elapsed"]),
                           distance=int(val["distance"]))


if __name__ == "__main__":
    url = "localhost:8080/v1/distances"
    for dist, i in zip(HttpDistanceClient(url).values(), range(10)):
        print(dist)
