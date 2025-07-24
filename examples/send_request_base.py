import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from optclient.solver_utils.ortools.client import Client

# from optclient.operations_research import linear_solver_pb2
# from optclient.operations_research.linprog_service_pb2_grpc import LinProgServiceStub


def create_sample_problem():
    model_request = Client.create_request()
    model = model_request.model

    objective_coefficients = [10.0, 6.0, 4.0]
    variable_names = ["x1", "x2", "x3"]
    constraint_names = ["c1", "c2", "c3"]
    constraint_upbound = [100.0, 600.0, 300.0]
    constraint_coefficients = [[1.0, 1.0, 1.0], [10.0, 4.0, 5.0], [2.0, 2.0, 6.0]]

    # Set up variables
    num_var = len(variable_names)
    for i in range(num_var):
        variable = model.variable.add()
        variable.name = variable_names[i]
        variable.objective_coefficient = objective_coefficients[i]
        variable.lower_bound = 0.0 
        variable.is_integer = False  

    model.maximize = True

    # Set up constraints
    num_cons = len(constraint_names)
    for i in range(num_cons):
        constraint = model.constraint.add()
        constraint.name = constraint_names[i]
        constraint.upper_bound = constraint_upbound[i]
        # dealing with the constraint coefficient 
        for j in range(num_var):
            constraint.coefficient.append(constraint_coefficients[i][j])
            constraint.var_index.append(j)
    # Set up solver 
    # model_request.solver_type  = linear_solver_pb2.MPModelRequest.SolverType.GLOP_LINEAR_PROGRAMMING

    return model_request


def send_and_solve_problem(model_request):
    client = Client(target="localhost:50051")
    response = client.send_request_via_insecure_channel(model_request)
    
    # if response.status.code != 0:
    #     raise Exception(f"Solver failed with status: {response.status.message}")
    
    print("The values of the variables:")
    variable_names = ["x1", "x2", "x3"]
    for j in range(3):
        print('Variable %s : %f' %(variable_names[j], response.variable_value[j]))
    print("The objective value : %f" %(response.objective_value))
    return 

if __name__ == "__main__":
    model_request = create_sample_problem()
    send_and_solve_problem(model_request)


