from __future__ import annotations
from dataclasses import dataclass

from typing import TYPE_CHECKING, Any, Optional

from enum import Enum, auto
from optclient.solver_utils.expression import LinExpr

if TYPE_CHECKING:
    from optclient.solver_utils.isolver import SolverT

class ConstrSense(Enum):
    leq = auto()
    geq = auto()
    eq = auto()


@dataclass(frozen=True)
class LinConstraint:
    expr: LinExpr
    rhs: float = 0.0
    name: Optional[str] = None
    sense: ConstrSense = ConstrSense.leq
    #lazy
    # soft
    # penalty


    def add_model(self, model: SolverT):
        self._model = model

    @property
    def constr(self) -> Any:
        return self._model.get_constr(self.name)