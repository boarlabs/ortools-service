from typing import Optional


from gurobipy import Var
from gurobipy import Model
from gurobipy import GRB

from solver_utils.ivariable import IVariable, VarType


class Variable(IVariable, Var):

    def __init__(
        self,
        model: Model,
        name: str,
        vtype: VarType,
        lower_bound: Optional[float],
        upper_bound: Optional[float],
    ):
        vtype_to_gurobi_map = {
            VarType.boolean: GRB.BINRARY,
            VarType.integer: GRB.INTEGER,
            VarType.real: GRB.CONTINOUS,
        }
        self._var = model.addVar(
            name=name,
            vtype=vtype_to_gurobi_map[vtype],
            lb=lower_bound or -GRB.INFINITY,
            ub=upper_bound or GRB.INFINITY,
        )



