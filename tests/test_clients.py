#!/usr/bin/env python3

import logging
import subprocess
import unittest
from threading import Thread

from utils import setup_logging

from distance_client import DistanceClient
from grpc_distance_server import run_server
from grpc_distance_server import stop_server
from http_distance_client import HttpDistanceClient

logger = logging.getLogger(__name__)

setup_logging()


class ClientTest(unittest.TestCase):
    def run_http_proxy(self):
        subprocess.call('go run http_proxy.go -stderrthreshold=INFO -logtostderr=true', shell=True)

    def setUp(self):
        Thread(target=run_server, args=(.1,)).start()
        # Thread(target=self.run_http_proxy).start()

    def tearDown(self):
        stop_server()

    def test_client(self):
        self.distance_client(5, 10, False)

    def test_http_client(self):
        self.http_distance_client(5, 10, False)

    def distance_client(self, repeat, size, print_vals):
        cnt = 0
        for i in range(repeat):
            print("Iteration {0}".format(i))
            with DistanceClient("127.0.0.1") as client:
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
            with HttpDistanceClient("127.0.0.1:8080") as client:
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
