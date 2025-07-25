from abc import ABC, abstractmethod
from enum import Enum, auto
from typing import Dict, Any, Optional, TypeVar, List

from optclient.solver_utils.variable import Variable, VarType
from optclient.solver_utils.constraint import LinConstraint, ConstrSense
from optclient.solver_utils.expression import LinExpr

class OptSense(Enum):
    maximize = auto()
    minimize = auto()


class ISolver(ABC):
    """
    the Isolver class is supposed to be the contract and
    interface of users of the solvers.
    """

    variables: Dict[str, Variable]
    expressions: Dict[str, LinExpr]
    constraints: Dict[str, LinConstraint]
    objectives: Dict[str, LinExpr]
  
    # Approach 1: Solid interface fully isolated from the solver implementation. 
     
    @abstractmethod
    def add_variable(self, variable: Variable) -> Variable:
        raise NotImplementedError
    
    @abstractmethod
    def get_variable(self, var_name: str) -> Variable:
        raise NotImplementedError
    
    @abstractmethod
    def get_variable_value(self, variable: Variable) -> float:
        raise NotImplementedError

    @abstractmethod
    def add_lin_constraint(
        self, 
        name: str,
        variables: List[Variable],
        coefficients: List[float],
        rhs: float,
        sense: ConstrSense,
    ):
        raise NotImplementedError
    
    @abstractmethod
    def add_linear_constraint(self, constraint: LinConstraint):
        raise NotImplementedError
        
    @abstractmethod
    def get_constraint(self, name: str) -> LinConstraint:
        raise NotImplementedError

    @abstractmethod
    def add_linear_expression(self, expr: LinExpr):
        raise NotImplementedError
    
    @abstractmethod
    def add_objective(self, term: LinExpr, name:str):
        raise NotImplementedError

    @abstractmethod
    def get_objective_value(self):
        raise NotImplementedError
    
    @abstractmethod
    def solve_model(self, sense: OptSense, options: Dict[str, Any]):
        raise NotImplementedError
    
    # common for both approache 1 and 2
    

    # Approach 2: Partial interface, where the solver implementation is
    #  implicittly exposed to users.
    # we need to make some implicit assumptions on what "common" solver
    # would behave

    @abstractmethod
    def get_var(self, var_name) -> Any:
        raise NotImplementedError

    @abstractmethod
    def add_constr(self, name: str, constraint: Any):
        raise NotImplementedError
    
    @abstractmethod
    def get_constr(self, name: str) -> Any:
        raise NotImplementedError
    
    
    @abstractmethod
    def add_objective_terms(self, objective_terms: Any):
        raise NotImplementedError
    


SolverT = TypeVar("SolverT", bound=ISolver)



#  that the "model" objects that would be created by specific solvers
#  would or would not be exposed to users?

#     if we want the model to have a list of 
#     variables and constraints, should we create them as attributes of the ISolver or not.
#     If I add them as atributes does it mean, that the other approach that deals with partial
#     interface would run into issues? 
#     would we need to define Any as type?

#     How do we define a constraint in interface? is a constraint (Ax<b), combo of a LinExpr and rhs?