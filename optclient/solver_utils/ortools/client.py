import grpc

from operations_research import linear_solver_pb2
from operations_research.linprog_service_pb2_grpc import LinProgServiceStub



class Client:
    def __init__(self, target):
        self.target = target
    
    @staticmethod
    def create_request() -> linear_solver_pb2.MPModelRequest:
        model_request= linear_solver_pb2.MPModelRequest()
        return  model_request

    def send_request_via_insecure_channel(self, request):
        with grpc.insecure_channel(self.target) as channel:
            stub = _create_stub(channel)
            response = _send_request_unary(stub, request)
            
        return response



def _create_stub(channel) -> LinProgServiceStub:
    stub = LinProgServiceStub(channel)
    return stub

def _send_request_unary(stub: LinProgServiceStub, request):
    response = stub.MILPModel(request)
    return  response