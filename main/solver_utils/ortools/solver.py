from typing import Dict
from collections import defaultdict

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

        self._model: linear_solver_pb2.MPModelProto =  _create_request()
        self._vars: Dict[str, linear_solver_pb2.MPVariableProto] = {}
        self._var_index: Dict[str, int] = defaultdict(int)
        self._model_response: linear_solver_pb2.MPSolutionResponse

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
        self._var_index[variable.name]
        return variable
    

    def get_variable(self, var_name: str) -> Variable:
        return self.variables[var_name]

    def get_var(self, var_name: str) -> linear_solver_pb2.MPVariableProto:
        return self._vars[var_name]

    def get_variable_value(self, variable: Variable) -> float:
        solution: linear_solver_pb2.MPSolutionResponse = self._model_response
        return solution.variable_value[self._var_index[variable.name]]
    
    def add_linear_expression(self, expr: LinExpr):
        self.expressions[expr.name] = expr

    def add_constr(self, name: str, constraint: Any):
        raise ValueError("this method is not applicable here")




def _create_request() -> linear_solver_pb2.MPModelProto:
    model_request= linear_solver_pb2.MPModelRequest()
    return  model_request.model


