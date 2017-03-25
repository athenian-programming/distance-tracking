#!/usr/bin/env python3

import logging
import unittest

from utils import setup_logging

from distance_client import DistanceClient
from http_distance_client import HttpDistanceClient

logger = logging.getLogger(__name__)

setup_logging()


class ClientTest(unittest.TestCase):
    def test_client(self):
        self.distance_client(5, 10, False)

    def test_http_client(self):
        self.http_distance_client(5, 10, False)

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
