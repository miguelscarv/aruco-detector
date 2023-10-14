import json
import aruco_pb2
import aruco_pb2_grpc
import grpc


IMAGE_PATH = "/Users/miguelcarvalho/Desktop/smart_retail/image_input/extracted_zip_files/1696340773190/5511_25.jpg"
camera_25 = {"fx": 533.3333333333334, "fy": 533.3333333333334, "cx": 640.0, "cy": 360.0, "resolution_x": 1280, "resolution_y": 720, "clip_start": 0.10000000149011612, "clip_end": 1000.0, "t": [0.043643027544021606, -0.2507721185684204, 3.4533329010009766], "R": [[-0.004169007297605276, -0.9997276663780212, -0.022955063730478287], [-0.999540388584137, 0.003476842539384961, 0.030110809952020645], [-0.030022799968719482, 0.02307005226612091, -0.999282956123352]], "distortion": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]}


with grpc.insecure_channel("companhia.isr.tecnico.ulisboa.pt:4500") as channel:
        stub = aruco_pb2_grpc.ArucoServiceStub(channel)

        try:

            with open(IMAGE_PATH, "rb") as f:
                img_bytes = f.read()
                res = stub.GetArUcoMarkers(aruco_pb2.Image(data=img_bytes, aux=json.dumps(camera_25)))
                print(res)


        except grpc.RpcError as rpc_error:
            print('An error has occurred:')
            print(f'  Error Code: {rpc_error.code()}')
            print(f'  Details: {rpc_error.details()}')