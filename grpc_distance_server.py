#!/usr/bin/env python

import argparse
import logging
import time

import grpc
from concurrent import futures
from grpc_support import GenericServer
from prometheus_client import Counter
from prometheus_client import start_http_server
from utils import current_time_millis
from utils import setup_logging

from proto.distance_service_pb2 import Distance
from proto.distance_service_pb2 import DistanceServiceServicer
from proto.distance_service_pb2 import ServerInfo
from proto.distance_service_pb2 import add_DistanceServiceServicer_to_server

logger = logging.getLogger(__name__)

REQUEST_COUNTER = Counter('getDistances_request_type_count', 'getDistances() request type count',
                          ['method', 'endpoint'])


class GrpcDistanceServer(DistanceServiceServicer, GenericServer):
    def __init__(self, port=None):
        super(GrpcDistanceServer, self).__init__(port=port, desc="distance server")
        self.grpc_server = None

    def registerClient(self, request, context):
        logger.info("Connected to %s client %s [%s]", self.desc, context.peer(), request.info)
        return ServerInfo(info="Server invoke count {0}".format(self.increment_cnt()))

    def getDistance(self, request, context):
        REQUEST_COUNTER.labels(method='get', endpoint='/v1/distance').inc()
        return self.get_currval()

    def getDistances(self, request, context):
        client_info = request.info
        # Update metrics
        REQUEST_COUNTER.labels(method='get', endpoint='/v1/distances').inc()
        return self.currval_generator(context.peer())

    def _init_values_on_start(self):
        self.write_distance(-1)

    def _start_server(self):
        logger.info("Starting gRPC %s listening on %s", self.desc, self.hostname)
        self.grpc_server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        add_DistanceServiceServicer_to_server(self, self.grpc_server)
        self.grpc_server.add_insecure_port(self.hostname)
        self.grpc_server.start()
        try:
            while not self.stopped:
                time.sleep(1)
        except KeyboardInterrupt:
            pass
        finally:
            self.stop()

    def write_distance(self, distance):
        if not self.stopped:
            self.id += 1
            self.set_currval(Distance(id=self.id,
                                      ts=current_time_millis(),
                                      distance=distance))


stopped = False


def run_server(delay):
    with GrpcDistanceServer() as server:
        cnt = 0
        while not stopped:
            server.write_distance(cnt)
            cnt += 1
            time.sleep(delay)


def stop_server():
    global stopped
    stopped = True


if __name__ == "__main__":
    setup_logging()

    parser = argparse.ArgumentParser()
    parser.add_argument("--delay", type=float, default=1.0, help="Delay secs")
    args = vars(parser.parse_args())

    # Start up a server to expose the metrics.
    start_http_server(8000)

    run_server(args["delay"])
