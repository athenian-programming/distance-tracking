import grpc

import grpc_server_pb2 as grpc__server__pb2


class DistanceServerStub(object):
    def __init__(self, channel):
        """Constructor.
    
        Args:
          channel: A grpc.Channel.
        """
        self.registerClient = channel.unary_unary(
            '/distance_tracking.DistanceServer/registerClient',
            request_serializer=grpc__server__pb2.ClientInfo.SerializeToString,
            response_deserializer=grpc__server__pb2.ServerInfo.FromString,
        )
        self.getDistances = channel.unary_stream(
            '/distance_tracking.DistanceServer/getDistances',
            request_serializer=grpc__server__pb2.ClientInfo.SerializeToString,
            response_deserializer=grpc__server__pb2.DistanceValue.FromString,
        )


class DistanceServerServicer(object):
    def registerClient(self, request, context):
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def getDistances(self, request, context):
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_DistanceServerServicer_to_server(servicer, server):
    rpc_method_handlers = {
        'registerClient': grpc.unary_unary_rpc_method_handler(
            servicer.registerClient,
            request_deserializer=grpc__server__pb2.ClientInfo.FromString,
            response_serializer=grpc__server__pb2.ServerInfo.SerializeToString,
        ),
        'getDistances': grpc.unary_stream_rpc_method_handler(
            servicer.getDistances,
            request_deserializer=grpc__server__pb2.ClientInfo.FromString,
            response_serializer=grpc__server__pb2.DistanceValue.SerializeToString,
        ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
        'distance_tracking.DistanceServer', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))
