#!/bin/sh
set -ex
wget https://github.com/google/protobuf/archive/v3.2.0-alpha-1.tar.gz
tar -xzvf v3.2.0-alpha-1.tar.gz
cd protobuf-3.2.0-alpha-1 && ./autogen && ./configure --prefix=/usr && make && sudo make install && sudo ldconfig

