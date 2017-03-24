#!/usr/bin/env python3

import logging
import unittest
from threading import Thread

from utils import setup_logging

from distance_client import DistanceClient
from http_distance_client import HttpDistanceClient

logger = logging.getLogger(__name__)

setup_logging()


class ClientTest(unittest.TestCase):
    def test_client(self):
        for t in range(5):
            print("Launching client thread: {0}".format(t))
            Thread(target=self.distance_client, args=(5, 10, False)).start()

    def test_http_client(self):
        for t in range(5):
            print("Launching http client thread: {0}".format(t))
            Thread(target=self.http_distance_client, args=(5, 10, False)).start()

    def distance_client(self, repeat, size, print_vals):
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

        self.assertEqual(cnt, repeat * size * 2)

    def http_distance_client(self, repeat, size, print_vals):
        cnt = 0
        for i in range(repeat):
            print("Iteration: {0}".format(i))
            with HttpDistanceClient("localhost:8080") as client:
                for d, j in zip(client.values(), range(size)):
                    if print_vals:
                        print(d)
                    cnt += 1

                for j in range(size):
                    if print_vals:
                        print(client.value())
                    cnt += 1

        self.assertEqual(cnt, repeat * size * 2)


if __name__ == '__main__':
    unittest.main()
