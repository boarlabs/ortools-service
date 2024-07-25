from abc import ABC, abstractmethod
from typing import Optional
from enum import Enum, auto

class VarType(Enum):
    boolean = auto()
    integer = auto()
    real = auto()

class IVariable(ABC):
    name: str
    vtype: VarType
    lower_bound: Optional[float]
    upper_bound: Optional[float]

    # @abstractmethod
    # def __init__(
    #     self,
    #     name: str,
    #     vtype: VarType,
    #     lower_bound: Optional[float] = None,
    #     upper_bound: Optional[float] = None,
    # ):
    #     raise NotImplementedError