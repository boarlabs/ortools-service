from abc import ABC
from enum import Enum, auto
from solver_utils.iexpression import ILinExpr


class ConstrSense(Enum):
    leq = auto()
    geq = auto()
    eq = auto()


class IConstraint(ABC):
    name: str
    expr: ILinExpr
    sense: ConstrSense
