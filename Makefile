default: all

go-stubs:
	protoc -I/usr/local/include -I. -I${GOPATH}/src -I${GOPATH}/src/github.com/googleapis/googleapis/ -I${HOME}/git/protobuf/src --go_out=,plugins=grpc:. ./pb/distance_server.proto

py-stubs:
	python -m grpc_tools.protoc -I. -I${GOPATH}/src/github.com/googleapis/googleapis -I${HOME}/git/protobuf/src --python_out=. --grpc_python_out=. ./pb/distance_server.proto

proxy:
	protoc -I/usr/local/include -I. -I${GOPATH}/src -I${GOPATH}/src/github.com/googleapis/googleapis/ -I${HOME}/git/protobuf/src --grpc-gateway_out=logtostderr=true:. ./pb/distance_server.proto

swag:
	cd pb; protoc -I/usr/local/include -I. -I${GOPATH}/src -I${GOPATH}/src/github.com/googleapis/googleapis/ -I${HOME}/git/protobuf/src --swagger_out=logtostderr=true:../swagger ./distance_server.proto

all: go-stubs py-stubs proxy swag
