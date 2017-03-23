#!/usr/bin/env python3

import argparse
import logging
import time

import grpc
from concurrent import futures
from grpc_support import GenericServer
from utils import current_time_millis
from utils import setup_logging

from pb.distance_server_pb2 import Distance
from pb.distance_server_pb2 import DistanceServerServicer
from pb.distance_server_pb2 import ServerInfo
from pb.distance_server_pb2 import add_DistanceServerServicer_to_server

logger = logging.getLogger(__name__)


class GrpcDistanceServer(DistanceServerServicer, GenericServer):
    def __init__(self, port=None):
        super(GrpcDistanceServer, self).__init__(port=port, desc="distance server")
        self.grpc_server = None

    def registerClient(self, request, context):
        logger.info("Connected to {0} client {1} [{2}]".format(self.desc, context.peer(), request.info))
        return ServerInfo(info="Server invoke count {0}".format(self.increment_cnt()))

    def getDistance(self, request, context):
        return self.get_currval()

    def getDistances(self, request, context):
        client_info = request.info
        return self.currval_generator(context.peer())

    def _init_values_on_start(self):
        self.write_distance(-1)

    def _adjust_currval(self, currval, start_time):
        if currval:
            currval.elapsed = current_time_millis() - start_time
        return currval

    def _start_server(self):
        logger.info("Starting gRPC {0} listening on {1}".format(self.desc, self.hostname))
        self.grpc_server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        add_DistanceServerServicer_to_server(self, self.grpc_server)
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
                                      elapsed=0,
                                      distance=distance))


if __name__ == "__main__":
    setup_logging()

    parser = argparse.ArgumentParser()
    parser.add_argument("--count", type=int, default=10000, help="Count")
    parser.add_argument("--delay", type=float, default=1.0, help="Delay")
    args = vars(parser.parse_args())

    with  GrpcDistanceServer() as server:
        for i in range(args["count"]):
            server.write_distance(i)
            time.sleep(args["delay"])
