GOSRC = ${GOPATH}/src
GOOGLEAPIS = ${GOPATH}/src/github.com/grpc-ecosystem/grpc-gateway/third_party/googleapis/
PBAPIS = ${HOME}/git/protobuf/src

.PHONY: swagger

default: codegen

codegen: py-stubs go-stubs go-proxy swagger

py-stubs:
	python -m grpc_tools.protoc -I. -I$(GOSRC) -I$(GOOGLEAPIS) -I$(PBAPIS) --python_out=. --grpc_python_out=. ./pb/distance_server.proto

go-stubs:
	protoc -I/usr/local/include -I. -I$(GOSRC) -I$(GOOGLEAPIS) -I$(PBAPIS) --go_out=,plugins=grpc:. ./pb/distance_server.proto

go-proxy:
	protoc -I/usr/local/include -I. -I$(GOSRC) -I$(GOOGLEAPIS) -I$(PBAPIS) --grpc-gateway_out=logtostderr=true:. ./pb/distance_server.proto

swagger:
	cd pb; protoc -I/usr/local/include -I. -I$(GOSRC) -I$(GOOGLEAPIS) -I$(PBAPIS) --swagger_out=logtostderr=true:../swagger ./distance_server.proto

install-common:
	git clone https://github.com/athenian-robotics/common-robotics.git ${HOME}/git/common-robotics

install-py:
	pip install -r requirements.txt
	pip install -r http-client-requirements.txt

install-go:
	go get -u github.com/grpc-ecosystem/grpc-gateway/protoc-gen-grpc-gateway
	go get -u github.com/grpc-ecosystem/grpc-gateway/protoc-gen-swagger
	go get -u github.com/golang/protobuf/protoc-gen-go
	go get -u google.golang.org/grpc

http_proxy:
	go run http_proxy.go -stderrthreshold=INFO -logtostderr=true &

test_client:
	./http_distance_client.py

test_server:
	./impl/grpc_distance_server.py --count 10000 --delay .1 &
