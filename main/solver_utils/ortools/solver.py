
from main.operations_research import linear_solver_pb2

from main.solver_utils.isolver import ISolver, OptSense
from main.solver_utils.variable import Variable, VarType
from main.solver_utils.constraint import ConstrSense, LinConstraint
from main.solver_utils.expression import LinExpr



class Solver(ISolver):

    def __init__(self,):
        self.variables = {}
        self.expressions = {}
        self.constraints = {}
        self.objectives = {}

        self._model =  _create_request()
        self._vars = {}


    def add_variable(self, variable: Variable) -> Variable:
        self.variables[variable.name] = variable

        var = self._model.variable.add()
        var.name = variable.name
        if variable.lower_bound is not None:
            var.lower_bound = variable.lower_bound
        if variable.upper_bound is not None:
            var.upper_bound = variable.upper_bound
        if variable.vtype != VarType.real:
            var.is_integer = True
        
        self._vars[variable.name] = var
        variable.add_model(self)
        return variable
    

    def get_variable(self, var_name: str) -> Variable:
        return self.variables[var_name]

    def get_var(self, var_name: str) -> linear_solver_pb2.MPVariableProto:
        return self._vars[var_name]
    


    def get_variable_value(self, variable: Variable) -> float:
        var = self.get_var(variable.name)
            return var.x

def _create_request() -> linear_solver_pb2.MPModelProto:
    model_request= linear_solver_pb2.MPModelRequest()
    return  model_request.model


