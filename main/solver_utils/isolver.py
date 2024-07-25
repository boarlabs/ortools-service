from abc import ABC, abstractmethod
from enum import Enum, auto
from typing import Dict, Any

from solver_utils.ivariable import IVariable
from solver_utils.iconstraint import IConstraint
from solver_utils.iexpression import ILinExpr

class OptSense(Enum):
    maximize = auto()
    minimize = auto()


class ISolver(ABC):
    """
    the Isolver class is supposed to be the contract and
    interface of users of the solvers. so there is the question
    that the "model" objects that would be created by specific solvers
    would or would not be exposed to users. ( I guess it should not)
    Also there is this question that if we want the model to have a list of 
    variables and constraints, should we create them as attributes of the ISolver or not.
    If I add them as atributes does it mean, that the other approach that deals with partial
    interface would run into issues? would we need to define Any as type?
    How do we define a constraint in interface? is a constraint (Ax<b), combo of a LinExpr and rhs?
    """

    variables: Dict[str, Any]
    expressions: Dict[str, Any]
    constraints: Dict[str, Any]
    objectives: Dict[str, Any]
    

    @abstractmethod
    def add_var(self, name, vtype, lower_bound, upper_bound):
        raise NotImplementedError
    
    @abstractmethod
    def add_constr(self, name, constraint):
        raise NotImplementedError
    
    @abstractmethod
    def add_variable(self, variable: IVariable):
        raise NotImplementedError
    
    @abstractmethod
    def add_lin_constraint(
        self, 
        name: str,
        vairables, 
        coefficients,
        rhs,
        #lazy
        # soft
        # penalty
    ):
        raise NotImplementedError
    
    @abstractmethod
    def add_constraint(self, constraint: IConstraint):
        raise NotImplementedError
        
    
    @abstractmethod
    def add_objective(self, term: ILinExpr):
        raise NotImplementedError

    
    @abstractmethod
    def add_objective_terms(self, objective_terms):
        raise NotImplementedError
    
    @abstractmethod
    def solve_model(self, sense, options):
        raise NotImplementedError
    
    @abstractmethod
    def get_objective_value(self):
        raise NotImplementedError
    
    @abstractmethod
    def get_constraint(self, name):
        raise NotImplementedError
    
    @abstractmethod
    def get_var_value(self, var):
        raise NotImplementedError