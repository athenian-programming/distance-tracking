import logging
import time

import grpc
from concurrent import futures
from grpc_support import GenericServer
from utils import current_time_millis

from gen.grpc_server_pb2 import DistanceServerServicer
from gen.grpc_server_pb2 import DistanceValue
from gen.grpc_server_pb2 import ServerInfo
from gen.grpc_server_pb2 import add_DistanceServerServicer_to_server

logger = logging.getLogger(__name__)


class DistanceServer(DistanceServerServicer, GenericServer):
    def __init__(self, port):
        super(DistanceServer, self).__init__(port, "position server")
        self._grpc_server = None

    def registerClient(self, request, context):
        logger.info("Connected to {0} client {1} [{2}]".format(self.desc, context.peer(), request.info))
        return ServerInfo(info="Server invoke count {0}".format(self.increment_cnt()))

    def getDistances(self, request, context):
        client_info = request.info
        return self.currval_generator(context.peer())

    def _init_values_on_start(self):
        self.write_distance(-1)

    def _start_server(self):
        logger.info("Starting gRPC {0} listening on {1}".format(self.desc, self._hostname))
        self._grpc_server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        add_DistanceServerServicer_to_server(self, self._grpc_server)
        self._grpc_server.add_insecure_port(self._hostname)
        self._grpc_server.start()
        try:
            while not self.stopped:
                time.sleep(1)
        except KeyboardInterrupt:
            pass
        finally:
            self.stop()

    def write_distance(self, distance):
        if not self.stopped:
            self.set_currval(DistanceValue(id=self._id, ts=current_time_millis, distance=distance))
            self._id += 1
