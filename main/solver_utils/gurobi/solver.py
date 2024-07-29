

from typing import Any, Dict, List, Union, cast, Optional
from main.solver_utils.constraint import LinConstraint, ConstrSense
from main.solver_utils.expression import LinExpr
from main.solver_utils.isolver import ISolver, OptSense
from main.solver_utils.variable import VarType, Variable

from gurobipy import Var   # type: ignore
from gurobipy import Model  # type: ignore
from gurobipy import GRB  # type: ignore
from gurobipy import Env  # type: ignore
from gurobipy import LinExpr as GRB_LinExpr   # type: ignore
from gurobipy import TempConstr   # type: ignore
from gurobipy import Constr   # type: ignore

CONSTR_SENSE_TO_GUROBI_MAP = {
    ConstrSense.eq: GRB.EQUAL,
    ConstrSense.leq: GRB.LESS_EQUAL,
    ConstrSense.geq: GRB.GREATER_EQUAL,
}
VTYPE_TO_GUROBI_MAP = {
    VarType.boolean: GRB.BINRARY,
    VarType.integer: GRB.INTEGER,
    VarType.real: GRB.CONTINOUS,
}
OPT_SENSE_TO_GUROBI_MAP = {
    OptSense.maximize: GRB.MAXIMIZE,
    OptSense.minimize: GRB.MINIMIZE,
}

class Solver(ISolver):
    def __init__(
        self,
    ):
        self.objectives = {}
        self.variables = {}
        self.expressions = {}
        self.constraints = {}

        self._vars: Dict[str, Var] = {}
        self._grb_exprs: Dict[str, GRB_LinExpr] = {}
        self._net_objective = GRB_LinExpr()
        self._model = Model("optimizaton_model", env=get_grb_env())

    
    def add_variable(self, variable: Variable) -> Variable:
        var = self._model.addVar(
            name=variable.name,
            vtype=VTYPE_TO_GUROBI_MAP[variable.vtype],
            lb=variable.lower_bound or -GRB.INFINITY,
            ub=variable.upper_bound or GRB.INFINITY,
        )
        self.variables[variable.name] = variable
        self._vars[variable.name] = var
        variable.add_model(self)   # I think we could go without this if needed
        return variable

    
    def get_variable(self, var_name: str) -> Variable:
        return self.variables[var_name]
    
    def get_var(self, var_name: str) -> Var:
        self._model.update() # do we need this also?
        return self._model.getVarByName(var_name)
    
    def get_variable_value(self, variable: Variable) -> float:
        var: Var = self.get_var(variable.name)
        self._model.update()
        return var.x

    def add_linear_expression(self, expr: LinExpr):
        self.expressions[expr.name] = expr
    
        self._grb_exprs[expr.name] = get_grb_expr(expr)

    def add_constr(self, name: str, constraint: TempConstr):
        self._model.addConstr(constraint, name)
    
    def get_constr(self, name: str) -> Constr:
        self._model.update()
        return self._model.getConstrByName(name)
    
    def get_constraint(self, name: str) -> LinConstraint:
        return self.constraints[name]
    
    def add_linear_constraint(self, constraint: LinConstraint):
        grb_expr= get_grb_expr(constraint.expr)
        self._model.addLConstr(
            lhs=grb_expr,
            sense=CONSTR_SENSE_TO_GUROBI_MAP[constraint.sense],
            rhs=constraint.rhs,
            name=constraint.name,
        )
    
    def add_lin_constraint(
        self, 
        name: str, 
        variables: List[Variable], 
        coefficients: List[float],
        rhs: float, 
        sense: ConstrSense,
    ):
        vars = [
            self._vars[variable.name] for variable in variables
        ]
        self._model.addLConstr(
            lhs=GRB_LinExpr(coefficients, vars),
            sense=CONSTR_SENSE_TO_GUROBI_MAP[sense],
            rhs=rhs,
            name=name,
        )
        self.constraints[name] = LinConstraint(
            name=name,
            expr=LinExpr(
                name=name,
                variables= cast(List[Union[Variable, LinExpr]] , variables),
                coefs=coefficients,
                const=0.0,
            ),
            rhs=rhs,
            sense=sense,
        )
    
    def add_objective_terms(self, objective_terms: GRB_LinExpr):
        self._net_objective += objective_terms

    def add_objective(self, term: LinExpr, name: str):
        """
        adds an objective term, a LinExpr which could contain multiple vars and terms,
        to the model with a given name,
        we add it to the overall objective of the model, and
        store it in the objective dictionary (for post-precces etc)
        the LinExpr itself could include a name for it, but we could
        name the objective differently (e.g. showing purpose of it, etc)
        """
        self.objectives[name] = term
        grb_expression = get_grb_expr(expr=term)
        self.add_objective_terms(grb_expression)
    

    def solve_model(self, sense: OptSense, options: Optional[Dict[str, Any]] = None):

        if options is not None:
            self._update_solver_params(options)
        self._model.setObjective(self._net_objective, OPT_SENSE_TO_GUROBI_MAP[OptSense])
        self._model.optimize()
    

    def _update_solver_params(self, options: Dict[str, Any]):
        # This method is a place holder for setting the parameters of the solver
        # for those parameters that could be set in special cases.
        # we do not wish to clearly specify what options/solver parameters
        # we would want to change, 
        # but it seems that at least for the usual ones like mipgap, timeout
        # gurobi has specific atributes
        if "mip_gap" in options.keys():
            self._model.Params.MIPGap = options["mip_gap"]

      

def get_grb_env(time_out: int = 400, priority: int = 0):
    return Env.ClientEnv(
        logfilename="",
        computeserver="",
        password="",
        priority=priority,
        time_out=time_out
    )

def get_grb_expr(expr: LinExpr) -> GRB_LinExpr:
    return (
        GRB_LinExpr(expr.const) 
        + GRB_LinExpr(
            list(expr.net_variable_coefs.values()),
            list(expr.net_variable_coefs.keys())
        )
    )




# so it seems that the current model, serves two ways of 
# creating a constraint, one, from the variables only
# two, from a linear constraint, that has a expression, and a rhs
# the creation of constraint from combo or vars, and exprs
# is really iterating the same thing needleslly, since in the expression
# defenition we have those covered, now we create constraints from expressions,
# and ceoffs given, if someone wants to create constraints the way Gurobi does
# we would need the other class for expression, and possibly another function for constraint.


# Question: how can we Enforce Type Checking in Runtime, the mypy does that
# staticly, but if the data is received from some API, without type, and
# maybe mypy is also supressed, then we lose safety