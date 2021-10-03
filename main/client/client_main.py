import logging
import sys
import grpc

from context import operations_research

# from operations_research.python.linprog_service_pb2_grpc import(
#     LinProgServiceStub
# )
from operations_research.linprog_service_pb2_grpc import(
    LinProgServiceStub
)

from client.basic_model_instantiation_from_proto import(
    instantiate_model
)




def create_stub(channel):
    stub = LinProgServiceStub(channel)
    return stub


def request_iterator(request):

    for item in request:
        yield item

def send_request(channel, request):
    stub = create_stub(channel)
    print(len(request))

    response = stub.MILPReferenceModel(request_iterator(request))
    solution_list = list()
    for solution in response:
        solution_list.append(solution)

    logging.info("client received response")
    return  





if __name__ == "__main__":

    # stub = create_stub()

    # model_requests = instantiate_model()


    logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
        )

    if len(sys.argv) > 1:
        target = sys.argv[1]
    else:
        target = '0.0.0.0:50051'

    # target = '3.128.179.93:50051'
    target = 'app.boarlabs.net:50051'


    request = instantiate_model()

    logging.info("client instantiated model")
    credentials = grpc.ssl_channel_credentials()


    with grpc.secure_channel(target, credentials) as channel:
        response = send_request(channel, request)
