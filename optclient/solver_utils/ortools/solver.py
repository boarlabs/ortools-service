from typing import Dict, Any, List, Optional, cast, Union, Tuple
from collections import defaultdict
from enum import Enum, auto

from optclient.operations_research import linear_solver_pb2

from optclient.solver_utils.isolver import ISolver, OptSense
from optclient.solver_utils.variable import Variable, VarType
from optclient.solver_utils.constraint import ConstrSense, LinConstraint
from optclient.solver_utils.expression import LinExpr
from optclient.solver_utils.ortools.client import Client


class  solvertypes(Enum):
    GLOP = auto()
    CBC = auto()
    GLPK = auto()
    SCIP = auto()

SOLVER_TYPES = dict(
    GLOP=linear_solver_pb2.MPModelRequest.SolverType.GLOP_LINEAR_PROGRAMMING,
    CBC=linear_solver_pb2.MPModelRequest.SolverType.CBC_MIXED_INTEGER_PROGRAMMING,
    GLPK=linear_solver_pb2.MPModelRequest.SolverType.GLPK_MIXED_INTEGER_PROGRAMMING,
    SCIP=linear_solver_pb2.MPModelRequest.SolverType.SCIP_MIXED_INTEGER_PROGRAMMING,
)

class Solver(ISolver):

    def __init__(self, client: Client):
        self.variables = {}
        self.expressions = {}
        self.constraints = {}
        self.objectives = {}

        self._client: Client = client
        self._request = _create_request()
        self._model: linear_solver_pb2.MPModelProto = self._request.model
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

    def add_objective_terms(self, objective_terms: List[Tuple[linear_solver_pb2.MPVariableProto, float]]):
        for var, obj_coef in objective_terms:
            var.objective_coefficient = obj_coef
    
    def add_objective(self, term: LinExpr, name: str):
        self.objectives[name] = term

        variables: Dict[Variable, float] = term.net_variable_coefs
        _vars: List[linear_solver_pb2.MPVariableProto] = [
            self._vars[variable.name] for variable in variables.keys()
        ]
        self.add_objective_terms(
            zip(_vars, variables.values())
        )
    
    def solve_model(self, sense: OptSense, options: Dict[str, Any]):

        self._set_opt_sense(sense)
        response = self._client.send_request_via_insecure_channel(self._request)
        self._model_response = response
        

    def _set_opt_sense(self, sense: OptSense):
        if sense == OptSense.maximize:
            self._model.maximize = True

    
    def _update_solver_params(self, options: Dict[str, Any]):
        if options["solver"]:
            self._request.solver_type = SOLVER_TYPES[options["solver"]]


def _create_request() -> linear_solver_pb2.MPModelRequest:
    model_request= linear_solver_pb2.MPModelRequest()
    return  model_request







