from typing import Dict, Any, List, Optional, cast, Union
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
        self._model_response: Optional[linear_solver_pb2.MPSolutionResponse] = None
        self._ortools_constrs: Dict[str, linear_solver_pb2.MPConstraintProto] = {}

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

    def add_constr(self, name: str, constraint: linear_solver_pb2.MPConstraintProto):
        self._ortools_constrs[name] = constraint
    
    def get_constr(self, name: str) -> linear_solver_pb2.MPConstraintProto:
        return self._ortools_constrs[name]
    
    def get_constraint(self, name: str) -> LinConstraint:
        return self.constraints[name]
    
    def add_linear_constraint(self, constraint: LinConstraint):
        self.constraints[constraint.name] = constraint
        constraint_net_variables = constraint.expr.net_variable_coefs
        rhs =  constraint.rhs - constraint.expr.net_constant
        _constr = self._add_constraint_to_model(
            constraint.name,
            constraint_net_variables.keys(),
            constraint_net_variables.values,
            rhs,
            constraint.sense,
        )
        self._ortools_constrs[constraint.name] = _constr

    def add_lin_constraint(
        self,
        name: str, 
        variables: List[Variable],
        coefficients: List[float], 
        rhs: float, 
        sense: ConstrSense,
    ):

        linear_constraint: LinConstraint = LinConstraint(
            name=name,
            expr=LinExpr(
                variables=cast(List[Union[Variable, LinExpr]], variables),
                coefs=coefficients,
                const=0.0,
                name=name,
            ),
            rhs=rhs,
            sense=sense,
        )
        self.constraints[name] = linear_constraint
        _constr = self._add_constraint_to_model(
            name,
            variables,
            coefficients,
            rhs,
            sense,
        )
        self._ortools_constrs[name] = _constr
            
    def _add_constraint_to_model(
        self,
        name: str,
        variables: List[Variable],
        coefficients: List[float],
        rhs: float,
        sense: ConstrSense,
    ) -> linear_solver_pb2.MPConstraintProto:
        
        _constr = self._model.constraint.add()
        _constr.name = name
        if sense == ConstrSense.leq:
            _constr.upper_bound = rhs
        elif sense == ConstrSense.geq:
            _constr.lower_bound = rhs
        elif sense == ConstrSense.eq:
            _constr.upper_bound = rhs
            _constr.lower_bound = rhs

        for variable, coef in zip(variables, coefficients):
            var_index = self._var_index[variable.name]
            _constr.var_index.append(var_index)
            _constr.coefficient.append(coef)
        
        return _constr


def _create_request() -> linear_solver_pb2.MPModelProto:
    model_request= linear_solver_pb2.MPModelRequest()
    return  model_request.model

