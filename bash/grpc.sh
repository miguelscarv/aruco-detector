#!/bin/bash

cd protos
python3 -m grpc_tools.protoc -I.  --python_out=. --grpc_python_out=. aruco.proto
mv *.py ../src