import os
import grpc
import app.location_pb2 as pb
import app.location_pb2_grpc as rpc

from app.config import config_by_name

CONFIG = config_by_name[os.getenv("ENV", "test")]
print("server ready on %s", CONFIG.APP_PORT)


channel = grpc.insecure_channel(f"127.0.0.1:{CONFIG.APP_PORT}")
stub = rpc.LocationServiceStub(channel)

location = pb.LocationMessage(
    person_id=5,
    longitude="37.747070",
    latitude="37.747070",
    creation_time="2024-11-17T16:15:30Z",
)

response = stub.Create(location)
print("Message sent! Response: ", response)
