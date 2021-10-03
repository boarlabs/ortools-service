import numpy as np
import pandas as pd

# from ..context import operations_research
from operations_research.linear_extension_pb2 import(
    ReferenceMPModel,
    ExtendedMPModel,
    ReferenceMPModelRequest,
)

from .basic_model_defenition_from_proto import(
    Generator,
    Load,
    Collection,
)

def instantiate_model():

    data_directory_path = "./data"
    data_file_name = "asset_data.xlsx"

    # Generator names in excel file are non-unique
    gen_data = pd.read_excel(f"{data_directory_path}/{data_file_name}", sheet_name="Generator")
    load_data = pd.read_excel(f"{data_directory_path}/{data_file_name}", sheet_name="Load", index_col=0)

    # Model
    instance = ReferenceMPModel(name= "problem_instance")
    instance.build_final = True

    # Sets
    # gen_index = set(gen_data.index)
    gen_index = range(5)
    # gen_names = [f"gen_name_{idx}" for idx in gen_index]
    gen_names = [f"gen_name_{idx}" for idx in range(5)]


    interval_index = set(load_data.index) ## check this

    ## Parameter Definition
    all_gen_params = [
        {   
            "name": gen_names[idx],
            "maxMW": np.minimum(gen_data["Pmax"][idx],gen_data["Available Capacity"][idx]),
            "minMW": np.minimum(gen_data["Pmin"][idx],gen_data["Available Capacity"][idx]),
            "max_ramp": gen_data["Ramp"][idx],
            "marginal_cost": gen_data["Price"][idx],
            "initial_commit": gen_data["Status"][idx],
        } for idx in gen_index
    ]

    load_params = {
        "name": "load_0",
        "load": 0.05 *load_data["Load Profile"] * 0.9 * gen_data["Available Capacity"].sum()
    }

    collection_params = {
        "name": "collection_0",
        "import_limit": 0,
        "export_limit": 0,
        "component_element_names": gen_names + ["load_0"]
    }

    ## Element addition
    gen_model_list = list()
    for idx in gen_index:
        gen_model = Generator(interval_index, all_gen_params[idx])

        gen_model_list.append(gen_model)
        instance.model_dependencies.extend([gen_model.mipmodel.name])

    load_model = Load(interval_index, load_params)
    instance.model_dependencies.extend([load_model.mipmodel.name])


    collection_model = Collection(interval_index, collection_params)
    instance.model_dependencies.extend([collection_model.mipmodel.name])

    ## Model construction

    # instance.build()
    model_request_list = list()

    for gen_model in gen_model_list:
        gen_model_extended = ExtendedMPModel()
        gen_model_request = ReferenceMPModelRequest()
        
        gen_model_extended.expression_model.CopyFrom(gen_model.mipmodel)
        gen_model_request.model.CopyFrom(gen_model_extended)

        model_request_list.append(gen_model_request)
    
    load_model_extended = ExtendedMPModel()
    load_model_request = ReferenceMPModelRequest()

    load_model_extended.concrete_model.CopyFrom(load_model.mipmodel)
    load_model_request.model.CopyFrom(load_model_extended)

    model_request_list.append(load_model_request)


    collection_model_extended = ExtendedMPModel()
    collection_model_request = ReferenceMPModelRequest()

    collection_model_extended.reference_model.CopyFrom(collection_model.mipmodel)
    collection_model_request.model.CopyFrom(collection_model_extended)

    model_request_list.append(collection_model_request)

    instance_model_extended = ExtendedMPModel()
    instance_model_request = ReferenceMPModelRequest()

    instance_model_extended.reference_model.CopyFrom(instance)
    instance_model_request.model.CopyFrom(instance_model_extended)

    model_request_list.append(instance_model_request)



    return model_request_list

# def solve_instance(instance):
#     opt = Solver()
#     opt.solve(instance, tee=True)

# def write_model_file(model, directory, filename, file_format="lp", symbolic_solver_labels=True):        
#         file_path = f"{directory}/{filename}.{file_format}"
#         model.write(file_path, io_options={"symbolic_solver_labels": symbolic_solver_labels})

# def write_model_formulation(model, file_path=None):
#     if file_path:
#         with open(file_path, "w") as file:
#             model.pprint(ostream=file)
#     else:
#         model.pprint()

# def get_results(model):
#     pyomo_objects = model.component_objects([pyo.Var, pyo.Expression, pyo.Param])
#     return {
#         obj.name: [[index, pyo.value(obj[index])] for index in obj] for obj in pyomo_objects
#     }
    

if __name__ == "__main__":


    model_requests = instantiate_model()
