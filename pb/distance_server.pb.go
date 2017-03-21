// Code generated by protoc-gen-go.
// source: pb/distance_server.proto
// DO NOT EDIT!

/*
Package distance_server is a generated protocol buffer package.

It is generated from these files:
	pb/distance_server.proto

It has these top-level messages:
	ClientInfo
	ServerInfo
	Distance
*/
package distance_server

import "github.com/golang/protobuf/proto"
import "fmt"
import "math"
import _ "google.golang.org/genproto/googleapis/api/annotations"
import google_protobuf1 "github.com/golang/protobuf/ptypes/empty"

import (
	"golang.org/x/net/context"
	"google.golang.org/grpc"
)

// Reference imports to suppress errors if they are not otherwise used.
var _ = proto.Marshal
var _ = fmt.Errorf
var _ = math.Inf

// This is a compile-time assertion to ensure that this generated file
// is compatible with the proto package it is being compiled against.
// A compilation error at this line likely means your copy of the
// proto package needs to be updated.
const _ = proto.ProtoPackageIsVersion2 // please upgrade the proto package

type ClientInfo struct {
	Info string `protobuf:"bytes,1,opt,name=info" json:"info,omitempty"`
}

func (m *ClientInfo) Reset() {
	*m = ClientInfo{}
}
func (m *ClientInfo) String() string {
	return proto.CompactTextString(m)
}
func (*ClientInfo) ProtoMessage() {}
func (*ClientInfo) Descriptor() ([]byte, []int) {
	return fileDescriptor0, []int{0}
}

func (m *ClientInfo) GetInfo() string {
	if m != nil {
		return m.Info
	}
	return ""
}

type ServerInfo struct {
	Info string `protobuf:"bytes,1,opt,name=info" json:"info,omitempty"`
}

func (m *ServerInfo) Reset() {
	*m = ServerInfo{}
}
func (m *ServerInfo) String() string {
	return proto.CompactTextString(m)
}
func (*ServerInfo) ProtoMessage() {}
func (*ServerInfo) Descriptor() ([]byte, []int) {
	return fileDescriptor0, []int{1}
}

func (m *ServerInfo) GetInfo() string {
	if m != nil {
		return m.Info
	}
	return ""
}

type Distance struct {
	Id       int32 `protobuf:"varint,1,opt,name=id" json:"id,omitempty"`
	Ts       int64 `protobuf:"varint,2,opt,name=ts" json:"ts,omitempty"`
	Elapsed  int64 `protobuf:"varint,3,opt,name=elapsed" json:"elapsed,omitempty"`
	Distance int32 `protobuf:"varint,4,opt,name=distance" json:"distance,omitempty"`
}

func (m *Distance) Reset() {
	*m = Distance{}
}
func (m *Distance) String() string {
	return proto.CompactTextString(m)
}
func (*Distance) ProtoMessage() {}
func (*Distance) Descriptor() ([]byte, []int) {
	return fileDescriptor0, []int{2}
}

func (m *Distance) GetId() int32 {
	if m != nil {
		return m.Id
	}
	return 0
}

func (m *Distance) GetTs() int64 {
	if m != nil {
		return m.Ts
	}
	return 0
}

func (m *Distance) GetElapsed() int64 {
	if m != nil {
		return m.Elapsed
	}
	return 0
}

func (m *Distance) GetDistance() int32 {
	if m != nil {
		return m.Distance
	}
	return 0
}

func init() {
	proto.RegisterType((*ClientInfo)(nil), "distance_server.ClientInfo")
	proto.RegisterType((*ServerInfo)(nil), "distance_server.ServerInfo")
	proto.RegisterType((*Distance)(nil), "distance_server.Distance")
}

// Reference imports to suppress errors if they are not otherwise used.
var _ context.Context
var _ grpc.ClientConn

// This is a compile-time assertion to ensure that this generated file
// is compatible with the grpc package it is being compiled against.
const _ = grpc.SupportPackageIsVersion4

// Client API for DistanceServer service

type DistanceServerClient interface {
	RegisterClient(ctx context.Context, in *ClientInfo, opts ...grpc.CallOption) (*ServerInfo, error)
	GetDistances(ctx context.Context, in *ClientInfo, opts ...grpc.CallOption) (DistanceServer_GetDistancesClient, error)
	GetDistance(ctx context.Context, in *google_protobuf1.Empty, opts ...grpc.CallOption) (*Distance, error)
	ResetElapsed(ctx context.Context, in *google_protobuf1.Empty, opts ...grpc.CallOption) (*google_protobuf1.Empty, error)
}

type distanceServerClient struct {
	cc *grpc.ClientConn
}

func NewDistanceServerClient(cc *grpc.ClientConn) DistanceServerClient {
	return &distanceServerClient{cc}
}

func (c *distanceServerClient) RegisterClient(ctx context.Context, in *ClientInfo, opts ...grpc.CallOption) (*ServerInfo, error) {
	out := new(ServerInfo)
	err := grpc.Invoke(ctx, "/distance_server.DistanceServer/registerClient", in, out, c.cc, opts...)
	if err != nil {
		return nil, err
	}
	return out, nil
}

func (c *distanceServerClient) GetDistances(ctx context.Context, in *ClientInfo, opts ...grpc.CallOption) (DistanceServer_GetDistancesClient, error) {
	stream, err := grpc.NewClientStream(ctx, &_DistanceServer_serviceDesc.Streams[0], c.cc, "/distance_server.DistanceServer/getDistances", opts...)
	if err != nil {
		return nil, err
	}
	x := &distanceServerGetDistancesClient{stream}
	if err := x.ClientStream.SendMsg(in); err != nil {
		return nil, err
	}
	if err := x.ClientStream.CloseSend(); err != nil {
		return nil, err
	}
	return x, nil
}

type DistanceServer_GetDistancesClient interface {
	Recv() (*Distance, error)
	grpc.ClientStream
}

type distanceServerGetDistancesClient struct {
	grpc.ClientStream
}

func (x *distanceServerGetDistancesClient) Recv() (*Distance, error) {
	m := new(Distance)
	if err := x.ClientStream.RecvMsg(m); err != nil {
		return nil, err
	}
	return m, nil
}

func (c *distanceServerClient) GetDistance(ctx context.Context, in *google_protobuf1.Empty, opts ...grpc.CallOption) (*Distance, error) {
	out := new(Distance)
	err := grpc.Invoke(ctx, "/distance_server.DistanceServer/getDistance", in, out, c.cc, opts...)
	if err != nil {
		return nil, err
	}
	return out, nil
}

func (c *distanceServerClient) ResetElapsed(ctx context.Context, in *google_protobuf1.Empty, opts ...grpc.CallOption) (*google_protobuf1.Empty, error) {
	out := new(google_protobuf1.Empty)
	err := grpc.Invoke(ctx, "/distance_server.DistanceServer/resetElapsed", in, out, c.cc, opts...)
	if err != nil {
		return nil, err
	}
	return out, nil
}

// Server API for DistanceServer service

type DistanceServerServer interface {
	RegisterClient(context.Context, *ClientInfo) (*ServerInfo, error)
	GetDistances(*ClientInfo, DistanceServer_GetDistancesServer) error
	GetDistance(context.Context, *google_protobuf1.Empty) (*Distance, error)
	ResetElapsed(context.Context, *google_protobuf1.Empty) (*google_protobuf1.Empty, error)
}

func RegisterDistanceServerServer(s *grpc.Server, srv DistanceServerServer) {
	s.RegisterService(&_DistanceServer_serviceDesc, srv)
}

func _DistanceServer_RegisterClient_Handler(srv interface{}, ctx context.Context, dec func(interface{}) error, interceptor grpc.UnaryServerInterceptor) (interface{}, error) {
	in := new(ClientInfo)
	if err := dec(in); err != nil {
		return nil, err
	}
	if interceptor == nil {
		return srv.(DistanceServerServer).RegisterClient(ctx, in)
	}
	info := &grpc.UnaryServerInfo{
		Server:     srv,
		FullMethod: "/distance_server.DistanceServer/RegisterClient",
	}
	handler := func(ctx context.Context, req interface{}) (interface{}, error) {
		return srv.(DistanceServerServer).RegisterClient(ctx, req.(*ClientInfo))
	}
	return interceptor(ctx, in, info, handler)
}

func _DistanceServer_GetDistances_Handler(srv interface{}, stream grpc.ServerStream) error {
	m := new(ClientInfo)
	if err := stream.RecvMsg(m); err != nil {
		return err
	}
	return srv.(DistanceServerServer).GetDistances(m, &distanceServerGetDistancesServer{stream})
}

type DistanceServer_GetDistancesServer interface {
	Send(*Distance) error
	grpc.ServerStream
}

type distanceServerGetDistancesServer struct {
	grpc.ServerStream
}

func (x *distanceServerGetDistancesServer) Send(m *Distance) error {
	return x.ServerStream.SendMsg(m)
}

func _DistanceServer_GetDistance_Handler(srv interface{}, ctx context.Context, dec func(interface{}) error, interceptor grpc.UnaryServerInterceptor) (interface{}, error) {
	in := new(google_protobuf1.Empty)
	if err := dec(in); err != nil {
		return nil, err
	}
	if interceptor == nil {
		return srv.(DistanceServerServer).GetDistance(ctx, in)
	}
	info := &grpc.UnaryServerInfo{
		Server:     srv,
		FullMethod: "/distance_server.DistanceServer/GetDistance",
	}
	handler := func(ctx context.Context, req interface{}) (interface{}, error) {
		return srv.(DistanceServerServer).GetDistance(ctx, req.(*google_protobuf1.Empty))
	}
	return interceptor(ctx, in, info, handler)
}

func _DistanceServer_ResetElapsed_Handler(srv interface{}, ctx context.Context, dec func(interface{}) error, interceptor grpc.UnaryServerInterceptor) (interface{}, error) {
	in := new(google_protobuf1.Empty)
	if err := dec(in); err != nil {
		return nil, err
	}
	if interceptor == nil {
		return srv.(DistanceServerServer).ResetElapsed(ctx, in)
	}
	info := &grpc.UnaryServerInfo{
		Server:     srv,
		FullMethod: "/distance_server.DistanceServer/ResetElapsed",
	}
	handler := func(ctx context.Context, req interface{}) (interface{}, error) {
		return srv.(DistanceServerServer).ResetElapsed(ctx, req.(*google_protobuf1.Empty))
	}
	return interceptor(ctx, in, info, handler)
}

var _DistanceServer_serviceDesc = grpc.ServiceDesc{
	ServiceName: "distance_server.DistanceServer",
	HandlerType: (*DistanceServerServer)(nil),
	Methods: []grpc.MethodDesc{
		{
			MethodName: "registerClient",
			Handler:    _DistanceServer_RegisterClient_Handler,
		},
		{
			MethodName: "getDistance",
			Handler:    _DistanceServer_GetDistance_Handler,
		},
		{
			MethodName: "resetElapsed",
			Handler:    _DistanceServer_ResetElapsed_Handler,
		},
	},
	Streams: []grpc.StreamDesc{
		{
			StreamName:    "getDistances",
			Handler:       _DistanceServer_GetDistances_Handler,
			ServerStreams: true,
		},
	},
	Metadata: "pb/distance_server.proto",
}

func init() {
	proto.RegisterFile("pb/distance_server.proto", fileDescriptor0)
}

var fileDescriptor0 = []byte{
	// 326 bytes of a gzipped FileDescriptorProto
	0x1f, 0x8b, 0x08, 0x00, 0x00, 0x00, 0x00, 0x00, 0x02, 0xff, 0x7c, 0x51, 0x4b, 0x4e, 0xc3, 0x30,
	0x10, 0x25, 0x69, 0x81, 0x32, 0x94, 0x80, 0x46, 0x08, 0x99, 0x94, 0x45, 0x95, 0x55, 0xc5, 0x22,
	0xe1, 0xb3, 0x63, 0x0b, 0x5d, 0x20, 0xb1, 0x2a, 0x12, 0x62, 0x07, 0x09, 0x99, 0x46, 0x96, 0x8a,
	0x1d, 0xd9, 0xa6, 0x12, 0x5b, 0xae, 0xc0, 0xd1, 0xb8, 0x02, 0x47, 0xe0, 0x00, 0x28, 0x4e, 0xdd,
	0x56, 0xad, 0xd2, 0x9d, 0x67, 0xde, 0xf8, 0xbd, 0x79, 0xf3, 0x80, 0x95, 0x59, 0x92, 0x73, 0x6d,
	0x52, 0xf1, 0x46, 0x2f, 0x9a, 0xd4, 0x94, 0x54, 0x5c, 0x2a, 0x69, 0x24, 0x1e, 0xae, 0xb4, 0xc3,
	0xb3, 0x42, 0xca, 0x62, 0x42, 0x49, 0x5a, 0xf2, 0x24, 0x15, 0x42, 0x9a, 0xd4, 0x70, 0x29, 0x74,
	0x3d, 0x1e, 0xf6, 0x66, 0xa8, 0xad, 0xb2, 0x8f, 0x71, 0x42, 0xef, 0xa5, 0xf9, 0xac, 0xc1, 0xa8,
	0x0f, 0x70, 0x3b, 0xe1, 0x24, 0xcc, 0xbd, 0x18, 0x4b, 0x44, 0x68, 0x73, 0x31, 0x96, 0xcc, 0xeb,
	0x7b, 0x83, 0xbd, 0x91, 0x7d, 0x57, 0x13, 0x8f, 0x56, 0xa6, 0x71, 0xe2, 0x15, 0x3a, 0x77, 0xb3,
	0x8d, 0x30, 0x00, 0x9f, 0xe7, 0x16, 0xdd, 0x1e, 0xf9, 0x3c, 0xaf, 0x6a, 0xa3, 0x99, 0xdf, 0xf7,
	0x06, 0xad, 0x91, 0x6f, 0x34, 0x32, 0xd8, 0xa5, 0x49, 0x5a, 0x6a, 0xca, 0x59, 0xcb, 0x36, 0x5d,
	0x89, 0x21, 0x74, 0x9c, 0x2f, 0xd6, 0xb6, 0xff, 0xe7, 0xf5, 0xd5, 0x9f, 0x0f, 0x81, 0x93, 0xa8,
	0x97, 0xc1, 0x07, 0x08, 0x14, 0x15, 0x5c, 0x1b, 0x52, 0xb5, 0x01, 0xec, 0xc5, 0xab, 0xe7, 0x5a,
	0x38, 0x0b, 0xd7, 0xc1, 0x85, 0xa9, 0x68, 0x0b, 0x33, 0xe8, 0x16, 0x64, 0x9c, 0x84, 0xde, 0xcc,
	0x75, 0xba, 0x06, 0xba, 0x8f, 0x11, 0xfb, 0xfa, 0xf9, 0xfd, 0xf6, 0x31, 0x3a, 0x48, 0xa6, 0x97,
	0xf3, 0xf4, 0xf4, 0x8d, 0x77, 0x7e, 0xe1, 0xe1, 0x13, 0xec, 0x2f, 0x69, 0xe0, 0x49, 0x5c, 0xe7,
	0x12, 0xbb, 0x5c, 0xe2, 0x61, 0x95, 0xcb, 0x26, 0xf6, 0x63, 0xcb, 0x1e, 0x60, 0x77, 0x99, 0x1d,
	0x9f, 0xa1, 0xab, 0x48, 0x93, 0x19, 0xce, 0x0e, 0xd9, 0x44, 0xdc, 0xd0, 0x77, 0x3b, 0xe3, 0x51,
	0xc5, 0xba, 0xcc, 0x94, 0xed, 0xd8, 0xc9, 0xeb, 0xff, 0x00, 0x00, 0x00, 0xff, 0xff, 0x80, 0xea,
	0x56, 0x47, 0x8b, 0x02, 0x00, 0x00,
}
