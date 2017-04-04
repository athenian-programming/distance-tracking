GOSRC = ${GOPATH}/src
GOOGLEAPIS = ${GOPATH}/src/github.com/grpc-ecosystem/grpc-gateway/third_party/googleapis/
PBAPIS = ${HOME}/git/protobuf/src

.PHONY: swagger

default: codegen

codegen: py-stubs go-stubs go-proxy swagger

py-stubs:
	python -m grpc_tools.protoc -I. -I$(GOSRC) -I$(GOOGLEAPIS) -I$(PBAPIS) --python_out=. --grpc_python_out=. ./proto/distance_service.proto

go-stubs:
	protoc -I/usr/local/include -I. -I$(GOSRC) -I$(GOOGLEAPIS) -I$(PBAPIS) --go_out=,plugins=grpc:. ./proto/distance_service.proto

go-proxy:
	protoc -I/usr/local/include -I. -I$(GOSRC) -I$(GOOGLEAPIS) -I$(PBAPIS) --grpc-gateway_out=logtostderr=true:. ./proto/distance_service.proto

swagger:
	cd proto; protoc -I/usr/local/include -I. -I$(GOSRC) -I$(GOOGLEAPIS) -I$(PBAPIS) --swagger_out=logtostderr=true:../swagger ./distance_service.proto

install-common:
	git clone https://github.com/athenian-robotics/common-robotics.git ${HOME}/git/common-robotics

install-py:
	pip install -r pip/requirements.txt
	pip install -r pip/http-client-requirements.txt

install-go:
	go get -u google.golang.org/grpc
	go get -u github.com/grpc-ecosystem/grpc-gateway/protoc-gen-grpc-gateway
	go get -u github.com/grpc-ecosystem/grpc-gateway/protoc-gen-swagger
#	go get -u github.com/golang/protobuf/protoc-gen-go
#	go get -u github.com/golang/protobuf/proto
	go get -u github.com/prometheus/client_golang/prometheus/promhttp

test_client:
	./http_distance_client.py

test_server:
	./grpc_distance_server.py --delay .1

http_proxy:
	go run http_proxy.go -stderrthreshold=INFO -logtostderr=true

