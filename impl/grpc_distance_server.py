import logging
import time

import grpc
from concurrent import futures
from google.protobuf.empty_pb2 import Empty
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
        super(GrpcDistanceServer, self).__init__(port=port, desc="position server")
        self.__start_time = current_time_millis()
        self.grpc_server = None

    def registerClient(self, request, context):
        logger.info("Connected to {0} client {1} [{2}]".format(self.desc, context.peer(), request.info))
        return ServerInfo(info="Server invoke count {0}".format(self.increment_cnt()))

    def resetElapsed(self, request, context):
        self.__start_time = current_time_millis()
        return Empty()

    def getDistance(self, request, context):
        return self.get_currval()

    def getDistances(self, request, context):
        client_info = request.info
        return self.currval_generator(context.peer())

    def _init_values_on_start(self):
        self.write_distance(-1)

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
            now = current_time_millis()
            self.set_currval(Distance(id=self.id,
                                      ts=now,
                                      elapsed=now - self.__start_time,
                                      distance=distance))
            self.id += 1


if __name__ == "__main__":
    setup_logging()

    with  GrpcDistanceServer() as server:
        for i in range(1000000):
            server.write_distance(i)
            time.sleep(1)
