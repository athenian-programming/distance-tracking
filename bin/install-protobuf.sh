#!/bin/sh
git clone https://github.com/google/protobuf
cd protobuf
./autogen
./configure
make
sudo make install
sudo ldconfig

