#!/usr/bin/env python3

import json

import requests
from utils import add_http_prefix


class Distance(object):
    def __init__(self, id, ts, elapsed, distance):
        self.id = id
        self.ts = ts
        self.elapsed = elapsed
        self.distance = distance

    def __str__(self):
        return "id: {0}\nts: {1}\nelapsed: {2}\ndistance: {3}\n".format(self.id, self.ts, self.elapsed, self.distance)


class HttpDistanceClient(object):
    def __init__(self, url):
        self.__url = add_http_prefix(url)

    def value(self):
        response = requests.get(self.__url + "/v1/distance", headers={"cache-control": "no-cache"})
        json_str = response.text
        val = json.loads(json_str)
        return Distance(id=int(val["id"]),
                        ts=int(val["ts"]),
                        elapsed=int(val["elapsed"]),
                        distance=int(val["distance"]))

    def values(self):
        response = requests.get(self.__url + "/v1/distances", headers={"cache-control": "no-cache"}, stream=True)
        for json_str in response.iter_lines():
            val = json.loads(json_str)["result"]
            yield Distance(id=int(val["id"]),
                           ts=int(val["ts"]),
                           elapsed=int(val["elapsed"]),
                           distance=int(val["distance"]))

    def resetElapsed(self):
        requests.get(self.__url + "/v1/resetElapsed", headers={"cache-control": "no-cache"})


if __name__ == "__main__":
    client = HttpDistanceClient("localhost:8080")
    for dist, i in zip(client.values(), range(10)):
        print(dist)
        if i % 5 == 0:
            client.resetElapsed()

    for i in range(10):
        print(client.value())
