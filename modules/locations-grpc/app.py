import os
import logging
from concurrent.futures import ThreadPoolExecutor
import grpc
from grpc_reflection.v1alpha import reflection
from time import perf_counter

import app.location_pb2_grpc as rpc
import app.location_pb2 as pb

from app.locations_grpc.services import LocationService


class TimingInterceptor(grpc.ServerInterceptor):
    def intercept_service(self, continuation, handler_call_details):
        start = perf_counter()
        try:
            return continuation(handler_call_details)
        finally:
            duration = perf_counter() - start
            name = handler_call_details.method
            logging.info("%s took %.3f seconds", name, duration)


def build_server(port):
    server = grpc.server(ThreadPoolExecutor())

    rpc.add_LocationServiceServicer_to_server(LocationService(), server)

    names = (
        pb.DESCRIPTOR.services_by_name["LocationService"].full_name,
        reflection.SERVICE_NAME,
    )
    reflection.enable_server_reflection(names, server)

    addr = f"[::]:{port}"
    server.add_insecure_port(addr)
    return server


if __name__ == "__main__":
    from app.config import config_by_name

    CONFIG = config_by_name[os.getenv("ENV", "test")]
    print("server ready on %s", CONFIG.APP_PORT)
    server = build_server(CONFIG.APP_PORT)
    server.start()

    server.wait_for_termination()
