import grpc 
import aruco_pb2
import aruco_pb2_grpc
import concurrent.futures as futures
import grpc_reflection.v1alpha.reflection as grpc_reflect
import io
from PIL import Image
import json
from vican.cam import Camera, estimate_pose_worker
from vican.geometry import SE3
import numpy as np

_SERVICE_NAME = 'ArucoService'

MARKER_SIZE = 0.48 * 0.575

aruco='DICT_4X4_1000'
marker_size=MARKER_SIZE
corner_refine='CORNER_REFINE_APRILTAG'
flags='SOLVEPNP_IPPE_SQUARE'
brightness=-150
contrast=120

def build_camera(v: dict) -> Camera:
    K = np.array([[v['fx'], 0.0, v['cx']],
                          [0.0, v['fy'], v['cy']],
                          [0.0, 0.0, 1.0]])
            
    cam = Camera(id=-1,
                intrinsics=K,
                distortion=np.array(v["distortion"]),
                extrinsics=SE3(R=np.array(v['R']),
                                t=np.array(v['t'])),
                resolution_x=v["resolution_x"],
                resolution_y=v["resolution_y"])

    return cam

def build_matrix(m):
    matrix = aruco_pb2.Matrix()

    for row in m:
        matrix.row.add().elements.extend(row)

    return matrix


class ArUcoServer(aruco_pb2_grpc.ArucoServiceServicer):

    def GetArUcoMarkers(self, request, context):

        image = Image.open(io.BytesIO(request.data))
        camera_intrinsics = json.loads(request.aux)
        camera = build_camera(camera_intrinsics)

        res = estimate_pose_worker( image=image,
                            cam=camera,
                            aruco='DICT_4X4_1000',
                            marker_size=MARKER_SIZE,
                            corner_refine='CORNER_REFINE_APRILTAG',
                            flags='SOLVEPNP_IPPE_SQUARE',
                            brightness=-150,
                            contrast=120 )

        markers = []
        for id in res:
            R = build_matrix(res[id]["R"])
            t = build_matrix(res[id]["t"])
            corners = build_matrix(res[id]["corners"])
            intrinsics = build_matrix(camera.intrinsics)
            
            mark = aruco_pb2.Marker(R=R, t=t, corners=corners, intrinsics=intrinsics, id=id)
            markers.append(mark)
        
        response = aruco_pb2.Response()
        response.markers.extend(markers)
        return response
            

def serve():
    server = grpc.server(futures.ThreadPoolExecutor())
    aruco_pb2_grpc.add_ArucoServiceServicer_to_server(
        ArUcoServer(),
        server)

    SERVICE_NAME = (
        aruco_pb2.DESCRIPTOR.services_by_name[_SERVICE_NAME].full_name,
        grpc_reflect.SERVICE_NAME
    )
    grpc_reflect.enable_server_reflection(SERVICE_NAME, server)
    server.add_insecure_port('[::]:8061')
    
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    serve()



