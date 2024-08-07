from __future__ import annotations
from dataclasses import dataclass
from typing import Optional, TYPE_CHECKING, Any
from enum import Enum, auto

if TYPE_CHECKING:
    from optclient.solver_utils.isolver import SolverT

class VarType(Enum):
    boolean = auto()
    integer = auto()
    real = auto()


@dataclass
class Variable:
    name: str
    vtype: VarType
    lower_bound: Optional[float] = None
    upper_bound: Optional[float] = None


    def add_model(self, model: SolverT):
        self._model = model
    
    @property
    def value(self) -> float:
        return self._model.get_variable_value(self)
    
    @property
    def var(self) -> Any:
        return self._model.get_var(self.name)



