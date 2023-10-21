# ArUco Detector

## Overview

This component can be used to detect ArUco markers in an image. It receives image bytes (data) as well as camera intrinsics and distortion parameters (stringified in aux) and outputs Rotation (R), Translation (t), ArUco corners (corners), and camera intrinsics (intrinsics) matrices together with the ArUco ID (id) and the projection error (error) for each ArUco detected. 

Certain parameters, like the contrast, brightenss and the ArUco dictionary, can be changed in `src/main.py` by changing the parameters of the `estimate_pose_worker` function call.

## Usage

The asset can be built with the following command:
```shell
$ docker build .
```
and it can be deployed using the command:
```
$ docker run -p 8061:8061 ARUCO
```
The `-p` flag is used to expose the 8061 docker port according to AI4EU specs.