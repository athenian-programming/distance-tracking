# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: pb/distance_server.proto

import sys

_b = sys.version_info[0] < 3 and (lambda x: x) or (lambda x: x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database

# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()

from google.api import annotations_pb2 as google_dot_api_dot_annotations__pb2
from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2

DESCRIPTOR = _descriptor.FileDescriptor(
    name='pb/distance_server.proto',
    package='distance_server',
    syntax='proto3',
    serialized_pb=_b(
        '\n\x18pb/distance_server.proto\x12\x0f\x64istance_server\x1a\x1cgoogle/api/annotations.proto\x1a\x1bgoogle/protobuf/empty.proto\"\x1a\n\nClientInfo\x12\x0c\n\x04info\x18\x01 \x01(\t\"\x1a\n\nServerInfo\x12\x0c\n\x04info\x18\x01 \x01(\t\"E\n\x08\x44istance\x12\n\n\x02id\x18\x01 \x01(\x05\x12\n\n\x02ts\x18\x02 \x01(\x03\x12\x0f\n\x07\x65lapsed\x18\x03 \x01(\x03\x12\x10\n\x08\x64istance\x18\x04 \x01(\x05\x32\xf1\x02\n\x0e\x44istanceServer\x12L\n\x0eregisterClient\x12\x1b.distance_server.ClientInfo\x1a\x1b.distance_server.ServerInfo\"\x00\x12_\n\x0cgetDistances\x12\x1b.distance_server.ClientInfo\x1a\x19.distance_server.Distance\"\x15\x82\xd3\xe4\x93\x02\x0f\x12\r/v1/distances0\x01\x12V\n\x0bgetDistance\x12\x16.google.protobuf.Empty\x1a\x19.distance_server.Distance\"\x14\x82\xd3\xe4\x93\x02\x0e\x12\x0c/v1/distance\x12X\n\x0cresetElapsed\x12\x16.google.protobuf.Empty\x1a\x16.google.protobuf.Empty\"\x18\x82\xd3\xe4\x93\x02\x12\x12\x10/v1/resetElapsedb\x06proto3')
    ,
    dependencies=[google_dot_api_dot_annotations__pb2.DESCRIPTOR, google_dot_protobuf_dot_empty__pb2.DESCRIPTOR, ])
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

_CLIENTINFO = _descriptor.Descriptor(
    name='ClientInfo',
    full_name='distance_server.ClientInfo',
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[
        _descriptor.FieldDescriptor(
            name='info', full_name='distance_server.ClientInfo.info', index=0,
            number=1, type=9, cpp_type=9, label=1,
            has_default_value=False, default_value=_b("").decode('utf-8'),
            message_type=None, enum_type=None, containing_type=None,
            is_extension=False, extension_scope=None,
            options=None),
    ],
    extensions=[
    ],
    nested_types=[],
    enum_types=[
    ],
    options=None,
    is_extendable=False,
    syntax='proto3',
    extension_ranges=[],
    oneofs=[
    ],
    serialized_start=104,
    serialized_end=130,
)

_SERVERINFO = _descriptor.Descriptor(
    name='ServerInfo',
    full_name='distance_server.ServerInfo',
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[
        _descriptor.FieldDescriptor(
            name='info', full_name='distance_server.ServerInfo.info', index=0,
            number=1, type=9, cpp_type=9, label=1,
            has_default_value=False, default_value=_b("").decode('utf-8'),
            message_type=None, enum_type=None, containing_type=None,
            is_extension=False, extension_scope=None,
            options=None),
    ],
    extensions=[
    ],
    nested_types=[],
    enum_types=[
    ],
    options=None,
    is_extendable=False,
    syntax='proto3',
    extension_ranges=[],
    oneofs=[
    ],
    serialized_start=132,
    serialized_end=158,
)

_DISTANCE = _descriptor.Descriptor(
    name='Distance',
    full_name='distance_server.Distance',
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[
        _descriptor.FieldDescriptor(
            name='id', full_name='distance_server.Distance.id', index=0,
            number=1, type=5, cpp_type=1, label=1,
            has_default_value=False, default_value=0,
            message_type=None, enum_type=None, containing_type=None,
            is_extension=False, extension_scope=None,
            options=None),
        _descriptor.FieldDescriptor(
            name='ts', full_name='distance_server.Distance.ts', index=1,
            number=2, type=3, cpp_type=2, label=1,
            has_default_value=False, default_value=0,
            message_type=None, enum_type=None, containing_type=None,
            is_extension=False, extension_scope=None,
            options=None),
        _descriptor.FieldDescriptor(
            name='elapsed', full_name='distance_server.Distance.elapsed', index=2,
            number=3, type=3, cpp_type=2, label=1,
            has_default_value=False, default_value=0,
            message_type=None, enum_type=None, containing_type=None,
            is_extension=False, extension_scope=None,
            options=None),
        _descriptor.FieldDescriptor(
            name='distance', full_name='distance_server.Distance.distance', index=3,
            number=4, type=5, cpp_type=1, label=1,
            has_default_value=False, default_value=0,
            message_type=None, enum_type=None, containing_type=None,
            is_extension=False, extension_scope=None,
            options=None),
    ],
    extensions=[
    ],
    nested_types=[],
    enum_types=[
    ],
    options=None,
    is_extendable=False,
    syntax='proto3',
    extension_ranges=[],
    oneofs=[
    ],
    serialized_start=160,
    serialized_end=229,
)

DESCRIPTOR.message_types_by_name['ClientInfo'] = _CLIENTINFO
DESCRIPTOR.message_types_by_name['ServerInfo'] = _SERVERINFO
DESCRIPTOR.message_types_by_name['Distance'] = _DISTANCE

ClientInfo = _reflection.GeneratedProtocolMessageType('ClientInfo', (_message.Message,), dict(
    DESCRIPTOR=_CLIENTINFO,
    __module__='pb.distance_server_pb2'
    # @@protoc_insertion_point(class_scope:distance_server.ClientInfo)
))
_sym_db.RegisterMessage(ClientInfo)

ServerInfo = _reflection.GeneratedProtocolMessageType('ServerInfo', (_message.Message,), dict(
    DESCRIPTOR=_SERVERINFO,
    __module__='pb.distance_server_pb2'
    # @@protoc_insertion_point(class_scope:distance_server.ServerInfo)
))
_sym_db.RegisterMessage(ServerInfo)

Distance = _reflection.GeneratedProtocolMessageType('Distance', (_message.Message,), dict(
    DESCRIPTOR=_DISTANCE,
    __module__='pb.distance_server_pb2'
    # @@protoc_insertion_point(class_scope:distance_server.Distance)
))
_sym_db.RegisterMessage(Distance)

try:
    # THESE ELEMENTS WILL BE DEPRECATED.
    # Please use the generated *_pb2_grpc.py files instead.
    import grpc
    from grpc.framework.common import cardinality
    from grpc.framework.interfaces.face import utilities as face_utilities
    from grpc.beta import implementations as beta_implementations
    from grpc.beta import interfaces as beta_interfaces


    class DistanceServerStub(object):

        def __init__(self, channel):
            """Constructor.
      
            Args:
              channel: A grpc.Channel.
            """
            self.registerClient = channel.unary_unary(
                '/distance_server.DistanceServer/registerClient',
                request_serializer=ClientInfo.SerializeToString,
                response_deserializer=ServerInfo.FromString,
            )
            self.getDistances = channel.unary_stream(
                '/distance_server.DistanceServer/getDistances',
                request_serializer=ClientInfo.SerializeToString,
                response_deserializer=Distance.FromString,
            )
            self.getDistance = channel.unary_unary(
                '/distance_server.DistanceServer/getDistance',
                request_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
                response_deserializer=Distance.FromString,
            )
            self.resetElapsed = channel.unary_unary(
                '/distance_server.DistanceServer/resetElapsed',
                request_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
                response_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
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

        def getDistance(self, request, context):
            context.set_code(grpc.StatusCode.UNIMPLEMENTED)
            context.set_details('Method not implemented!')
            raise NotImplementedError('Method not implemented!')

        def resetElapsed(self, request, context):
            context.set_code(grpc.StatusCode.UNIMPLEMENTED)
            context.set_details('Method not implemented!')
            raise NotImplementedError('Method not implemented!')


    def add_DistanceServerServicer_to_server(servicer, server):
        rpc_method_handlers = {
            'registerClient': grpc.unary_unary_rpc_method_handler(
                servicer.registerClient,
                request_deserializer=ClientInfo.FromString,
                response_serializer=ServerInfo.SerializeToString,
            ),
            'getDistances': grpc.unary_stream_rpc_method_handler(
                servicer.getDistances,
                request_deserializer=ClientInfo.FromString,
                response_serializer=Distance.SerializeToString,
            ),
            'getDistance': grpc.unary_unary_rpc_method_handler(
                servicer.getDistance,
                request_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
                response_serializer=Distance.SerializeToString,
            ),
            'resetElapsed': grpc.unary_unary_rpc_method_handler(
                servicer.resetElapsed,
                request_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
                response_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
            ),
        }
        generic_handler = grpc.method_handlers_generic_handler(
            'distance_server.DistanceServer', rpc_method_handlers)
        server.add_generic_rpc_handlers((generic_handler,))


    class BetaDistanceServerServicer(object):
        """The Beta API is deprecated for 0.15.0 and later.
    
        It is recommended to use the GA API (classes and functions in this
        file not marked beta) for all further purposes. This class was generated
        only to ease transition from grpcio<0.15.0 to grpcio>=0.15.0."""

        def registerClient(self, request, context):
            context.code(beta_interfaces.StatusCode.UNIMPLEMENTED)

        def getDistances(self, request, context):
            context.code(beta_interfaces.StatusCode.UNIMPLEMENTED)

        def getDistance(self, request, context):
            context.code(beta_interfaces.StatusCode.UNIMPLEMENTED)

        def resetElapsed(self, request, context):
            context.code(beta_interfaces.StatusCode.UNIMPLEMENTED)


    class BetaDistanceServerStub(object):
        """The Beta API is deprecated for 0.15.0 and later.
    
        It is recommended to use the GA API (classes and functions in this
        file not marked beta) for all further purposes. This class was generated
        only to ease transition from grpcio<0.15.0 to grpcio>=0.15.0."""

        def registerClient(self, request, timeout, metadata=None, with_call=False, protocol_options=None):
            raise NotImplementedError()

        registerClient.future = None

        def getDistances(self, request, timeout, metadata=None, with_call=False, protocol_options=None):
            raise NotImplementedError()

        def getDistance(self, request, timeout, metadata=None, with_call=False, protocol_options=None):
            raise NotImplementedError()

        getDistance.future = None

        def resetElapsed(self, request, timeout, metadata=None, with_call=False, protocol_options=None):
            raise NotImplementedError()

        resetElapsed.future = None


    def beta_create_DistanceServer_server(servicer, pool=None, pool_size=None, default_timeout=None,
                                          maximum_timeout=None):
        """The Beta API is deprecated for 0.15.0 and later.
    
        It is recommended to use the GA API (classes and functions in this
        file not marked beta) for all further purposes. This function was
        generated only to ease transition from grpcio<0.15.0 to grpcio>=0.15.0"""
        request_deserializers = {
            ('distance_server.DistanceServer', 'getDistance'): google_dot_protobuf_dot_empty__pb2.Empty.FromString,
            ('distance_server.DistanceServer', 'getDistances'): ClientInfo.FromString,
            ('distance_server.DistanceServer', 'registerClient'): ClientInfo.FromString,
            ('distance_server.DistanceServer', 'resetElapsed'): google_dot_protobuf_dot_empty__pb2.Empty.FromString,
        }
        response_serializers = {
            ('distance_server.DistanceServer', 'getDistance'): Distance.SerializeToString,
            ('distance_server.DistanceServer', 'getDistances'): Distance.SerializeToString,
            ('distance_server.DistanceServer', 'registerClient'): ServerInfo.SerializeToString,
            ('distance_server.DistanceServer',
             'resetElapsed'): google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
        }
        method_implementations = {
            ('distance_server.DistanceServer', 'getDistance'): face_utilities.unary_unary_inline(servicer.getDistance),
            ('distance_server.DistanceServer', 'getDistances'): face_utilities.unary_stream_inline(
                servicer.getDistances),
            ('distance_server.DistanceServer', 'registerClient'): face_utilities.unary_unary_inline(
                servicer.registerClient),
            ('distance_server.DistanceServer', 'resetElapsed'): face_utilities.unary_unary_inline(
                servicer.resetElapsed),
        }
        server_options = beta_implementations.server_options(request_deserializers=request_deserializers,
                                                             response_serializers=response_serializers,
                                                             thread_pool=pool, thread_pool_size=pool_size,
                                                             default_timeout=default_timeout,
                                                             maximum_timeout=maximum_timeout)
        return beta_implementations.server(method_implementations, options=server_options)


    def beta_create_DistanceServer_stub(channel, host=None, metadata_transformer=None, pool=None, pool_size=None):
        """The Beta API is deprecated for 0.15.0 and later.
    
        It is recommended to use the GA API (classes and functions in this
        file not marked beta) for all further purposes. This function was
        generated only to ease transition from grpcio<0.15.0 to grpcio>=0.15.0"""
        request_serializers = {
            ('distance_server.DistanceServer',
             'getDistance'): google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
            ('distance_server.DistanceServer', 'getDistances'): ClientInfo.SerializeToString,
            ('distance_server.DistanceServer', 'registerClient'): ClientInfo.SerializeToString,
            ('distance_server.DistanceServer',
             'resetElapsed'): google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
        }
        response_deserializers = {
            ('distance_server.DistanceServer', 'getDistance'): Distance.FromString,
            ('distance_server.DistanceServer', 'getDistances'): Distance.FromString,
            ('distance_server.DistanceServer', 'registerClient'): ServerInfo.FromString,
            ('distance_server.DistanceServer', 'resetElapsed'): google_dot_protobuf_dot_empty__pb2.Empty.FromString,
        }
        cardinalities = {
            'getDistance': cardinality.Cardinality.UNARY_UNARY,
            'getDistances': cardinality.Cardinality.UNARY_STREAM,
            'registerClient': cardinality.Cardinality.UNARY_UNARY,
            'resetElapsed': cardinality.Cardinality.UNARY_UNARY,
        }
        stub_options = beta_implementations.stub_options(host=host, metadata_transformer=metadata_transformer,
                                                         request_serializers=request_serializers,
                                                         response_deserializers=response_deserializers,
                                                         thread_pool=pool, thread_pool_size=pool_size)
        return beta_implementations.dynamic_stub(channel, 'distance_server.DistanceServer', cardinalities,
                                                 options=stub_options)
except ImportError:
    pass
# @@protoc_insertion_point(module_scope)
